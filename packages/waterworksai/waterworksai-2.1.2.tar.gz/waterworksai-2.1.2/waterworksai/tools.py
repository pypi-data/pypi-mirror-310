import geopandas as gpd
import pandas as pd
import requests
import json
import numpy as np

class PipeNetwork:
    def __init__(self, pipe_gdf):
        """
        Initialize the PipeNetwork class with a GeoDataFrame.
        :param geodataframe: GeoDataFrame containing pipe network data.
        """
        if not isinstance(pipe_gdf, gpd.GeoDataFrame):
            raise TypeError("Input must be a GeoDataFrame.")
        if pipe_gdf.empty:
            raise ValueError("The provided GeoDataFrame is empty.")

        self.network = pipe_gdf.to_crs('epsg:4326')

    def get_lof(self, api_key, id_col, construction_col, renovation_col, material_col, dimension_col, length_col):
        """
        Uses the API endpoint to get a Likelihood-of-failure estimation
        :return: geodataframe with LoF column.
        """
        pipe_network_ = self.network.drop(['geometry'], axis=1)
        x = requests.post('https://www.waterworks.ai/api/pipenetwork/lof',
                          json={'df': pipe_network_.to_json(orient='records', date_format='iso'), 'api_key': api_key,
                                'id': id_col,
                                'construction': construction_col, 'renovation': renovation_col,
                                'material': material_col,
                                'dimension': dimension_col, 'length': length_col})
        js = x.json()
        df_lof = pd.read_json(json.dumps(js), orient='records')
        df_lof = df_lof.set_index(id_col)
        gdf_lof = self.network.set_index(id_col)
        gdf_lof['LoF'] = df_lof['LoF']
        gdf_lof = gdf_lof.reset_index()

        return gdf_lof

    def get_cof(self, api_key, id_col, dimension_col):
        """
        Uses the API endpoint to get a Consequence-of-failure estimation
        :return: geodataframe with CoF column.
        """
        pipe_network_ = self.network
        cof = requests.post('https://www.waterworks.ai/api/pipenetwork/cof',
                            json={'bounds': pipe_network_.total_bounds.tolist(), 'api_key': api_key})
        js = cof.json()
        gdf_cof = gpd.GeoDataFrame.from_features(js['features'])
        join = gpd.sjoin(pipe_network_, gdf_cof)
        join = join[[id_col, 'CoF']].groupby(id_col).max()
        pipe_network_ = pipe_network_.set_index(id_col)
        pipe_network_['CoF'] = join['CoF']
        pipe_network_ = pipe_network_.reset_index()
        pipe_network_['CoF'] = pipe_network_['CoF'].fillna(0) # 0 where no environmental risks exist
        from sklearn.preprocessing import MinMaxScaler
        scaler = MinMaxScaler()
        pipe_network_[['dim_scaled']] = scaler.fit_transform(
            pipe_network_[[dimension_col]])
        pipe_network_['CoF'] = pipe_network_['CoF'] + (0.5*pipe_network_['dim_scaled']) # add dimension as CoF-parameter
        pipe_network_[['CoF']] = scaler.fit_transform(
            pipe_network_[['CoF']])

        return pipe_network_

    def get_rof(self, gdf_lof, gdf_cof, id_col):
        """
        Takes (prior) LoF and CoF calculations (geodataframes) and calculates risk-of-failure (RoF).
        :return: geodataframe with RoF column.
        """
        gdf_rof = gdf_lof.set_index(id_col)
        gdf_cof = gdf_cof.set_index(id_col)

        gdf_rof['CoF'] = gdf_cof['CoF']
        gdf_rof['RoF'] = gdf_rof['LoF']*gdf_rof['CoF']
        gdf_rof = gdf_rof.reset_index()

        return gdf_rof

    def get_renewal_need(self, renewal_rate, gdf_lof, gdf_rof, id_col, material_col, length_col):
        """
        Takes LoF and RoF calculations (geodataframes), a renewal rate (%) and names for id, material and length columns.
        :return: geodataframes with annual renewal need (per material) and pipes to be included in 5-year plan.
        """
        df = gdf_lof.copy()
        tot_len = df[length_col].sum()
        rr = 0.01 * renewal_rate
        renewal = round(rr * tot_len)
        years = np.arange(1, 50, 1)
        ids = []
        df_all = pd.DataFrame(columns=['Year', 'Material', 'Renewal Need (km)'])
        for mat in df[material_col].unique().tolist():
            renewal_needs = []
            for yr in years:
                df = df.sort_values(by=['RUL'])
                df['cs'] = df[length_col].cumsum()
                df['RUL'] = df['RUL'] - 1
                need = df.loc[df['RUL'] <= 0]  # [length_col].sum() / 1000
                rel_need = need.loc[need[material_col] == mat][length_col].sum() / 1000
                renewal_needs.append(rel_need)
                df.loc[df['cs'] < renewal, 'RUL'] = 100
                if yr <= 5:
                    ids.extend(need[id_col].tolist())

            df_plot = pd.DataFrame()
            df_plot['Year'] = years
            df_plot['Year'] = 2024 + df_plot['Year']
            df_plot['Material'] = mat
            df_plot['Renewal Need (km)'] = renewal_needs

            df_all = pd.concat([df_all, df_plot])

        five_year_plan = gdf_rof.loc[gdf_rof[id_col].isin(ids)]
        five_year_plan = five_year_plan.sort_values(by=['RoF'], ascending=False)

        return df_all, five_year_plan
