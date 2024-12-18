import numpy as np
import pandas as pd
import plotly.express as px
from plotly.offline import plot
import itertools
from itertools import combinations
from re import match


class Report:

    def __init__(self,file_path, target_feature):
        self.file_path = file_path
        self.target_feature = target_feature

    # reading the file and create DataFrame
    def read_df(self):
        df = pd.read_csv(self.file_path)

        # remove id col if present
        id_col = list(filter(lambda x: match('.*id', x), df.columns ))
        df = df.drop(id_col, axis=1)

        return df
    
    # divide the feature columns based on their dtype, i.e numerical, categorical, datetime
    def feature_segment(self):
        df = df = self.read_df()

        # Iterate through each column of the DataFrame
        for column in df.columns:
            # Check if the data type of the column is datetime
            if df[column].dtype == 'datetime64[ns]' :
            # Check if all the values in the column are of the correct format
                try:
                    pd.to_datetime(df[column])
                except ValueError:
                    # If any value in the column is not of the correct format, print a message indicating that the column is misclassified
                    continue
            elif df[column].dtype == 'object':
                try:
                    df[column] = pd.to_datetime(df[column])
                except ValueError:
                    # If any value in the column is not of the correct format, print a message indicating that the column is misclassified
                    continue

        num_cols = list(df.select_dtypes(include=['int64', 'int32', 'float64', 'float32']).columns)
        cat_cols = list(df.select_dtypes(include=['object']).columns)
        datetime_cols = list(df.select_dtypes(include=['datetime64[ns]']).columns)
        
        for col in reversed(num_cols):
            if 1 < df[col].nunique() < 15:
                num_cols.remove(col)
                cat_cols.append(col)
    
        return num_cols, cat_cols, datetime_cols
    
    #  return the basic details of data  i.e shape, num.shape etc
    def basic_data_details(self):
        df = self.read_df()
        null_counts = df.isnull().sum().sum()
        num_col, cat_col, datetime_col = self.feature_segment()
        num_col_shape = len(num_col)
        cat_col_shape = len(cat_col)
        datetime_col_shape = len(datetime_col)
        duplicate_records = df.duplicated().sum()
        return {'data_shape': df.shape, 'num_col_shape':num_col_shape, 'cat_col_shape':cat_col_shape, 'datetime_col_shape': datetime_col_shape,'null_counts':null_counts , 'duplicate_records':duplicate_records}
    
    def nullColChart(self) :
        df = self.read_df()
        null_counts = {}
        for col in df.columns:
            null_counts[col] = df[col].isnull().sum()
    
        if len(df.columns) >12:
            null_counts = dict(sorted(null_counts.items(), key= lambda x: x[1], reverse=True)[:12])
        else:
            null_counts
        null_counts = {'labels': list(null_counts.keys()), 'data': list(null_counts.values())}

        if np.cumsum(null_counts.get('data'))[-1] > 0:
            null_counts = null_counts
        else:
            null_counts = None
        return null_counts

    # Univarite| Bar: get the categorical(or limited unique value from numerical) columns detail for plotting bar chart.
    def get_unibarChart(self):
        df = self.read_df()
        col_size = df.shape[1]
        num_col, cat_col, datetime_col = self.feature_segment()
        limited_cat_cols = [col for col in cat_col if (df[col].nunique() < 15) and (df[col].nunique() >= 2) ]

        if len(limited_cat_cols) == 0:
            pass
        else:
            ret_dict = {}
            for col in limited_cat_cols:
                dt = df[col].value_counts().to_dict()
                ret_dict[col] = {'labels': list(dt.keys()), 'data': list(dt.values())}
            return ret_dict
        
    # Univarite| Violin: get the numerical columns detail for plotting violin chart.
    def get_univiolinChart(self):
        df = self.read_df()
        num_col, cat_col, datetime_col = self.feature_segment()

        voilin_plot_col = [col for col in num_col if (df[col].std() > 5) and (max(df[col].value_counts().to_dict().values()) / df.shape[0] > 0.5 )]
        violin_plots = []
        if len(voilin_plot_col) > 0:
            for col in voilin_plot_col:
                # print(col)
                fig = px.violin(df,y=col)
                fig.update_layout(
                            margin=dict(l=0, r=0, b=0, t=0, pad=0),
                            template="simple_white")
                violin_plt = plot(fig, output_type="div")
                violin_plots.append(violin_plt)

        
        return violin_plots
    
    # Univarite| Histplot: get the numerical columns detail for plotting histogram chart.
    def get_unihistChart(self):
        df = self.read_df()
        num_col, cat_col, datetime_col = self.feature_segment()
        voilin_plot_col = [col for col in num_col if (df[col].std() > 5) and (max(df[col].value_counts().to_dict().values()) / df.shape[0] > 0.5 )]
        hist_plot_col = [col for col in num_col if (df[col].std() > 5) and (col not in voilin_plot_col)]
        hist_plots = []
        if len(hist_plot_col) > 0:
            for col in hist_plot_col:
                # print(col)
                fig = px.histogram(df,x=col, nbins=16)
                fig.update_layout(
                            margin=dict(l=0, r=0, b=0, t=0, pad=0),
                            template="simple_white")
                hist_plt = plot(fig, output_type="div")
                hist_plots.append(hist_plt)

        
        return hist_plots
    
    # Bivarite| Boxplot: get the numerical columns detail for plotting histogram chart.
    def get_biboxplot(self):
        df = self.read_df()
        num_col, cat_col, datetime_col = self.feature_segment()
        voilin_plot_col = [col for col in num_col if (df[col].std() > 5) and (max(df[col].value_counts().to_dict().values()) / df.shape[0] > 0.5 )]
        hist_plot_col = [col for col in num_col if (df[col].std() > 5) and (col not in voilin_plot_col)]
        limited_cat_cols = [col for col in cat_col if (df[col].nunique() < 15) and (df[col].nunique() >= 2) ]
        
        
        # x_axis = limited_cat_cols
        # y_axis = hist_plot_col, if hist_plot_col <= 2 then y_axis = num_col
    
        if len(hist_plot_col) <=2 :
            y_axis_col = num_col
            
        else:
            y_axis_col = hist_plot_col


        if self.target_feature is None: 
            box_plots = []
            if len(limited_cat_cols)>0 and len(y_axis_col)>0:
                comb_col = list(itertools.product(limited_cat_cols, y_axis_col))

                for col in comb_col:
                    fig = px.box(df, x=col[0], y= col[1])
                    fig.update_layout(
                                margin=dict(l=0, r=0, b=0, t=0, pad=0),
                                template="simple_white")
                    box_plt = plot(fig, output_type="div")
                    box_plots.append(box_plt)
            return box_plots
        else:
            box_plots = []
            if self.target_feature in limited_cat_cols:
                limited_cat_cols.remove(self.target_feature)
            else :
                limited_cat_cols = limited_cat_cols
            if len(limited_cat_cols)>0 and len(y_axis_col)>0:
                comb_col = list(itertools.product(limited_cat_cols, y_axis_col))

                for col in comb_col:
                    fig = px.box(df, x=col[0], y= col[1], color=self.target_feature)
                    fig.update_layout(
                                margin=dict(l=0, r=0, b=0, t=0, pad=0),
                                template="simple_white")
                    box_plt = plot(fig, output_type="div")
                    box_plots.append(box_plt)
            return box_plots
            
        # box_plots = []
        # if len(limited_cat_cols)>0 and len(y_axis_col)>0:
        #     comb_col = list(itertools.product(limited_cat_cols, y_axis_col))

        #     for col in comb_col:
        #         fig = px.box(df, x=col[0], y= col[1])
        #         fig.update_layout(
        #                     margin=dict(l=0, r=0, b=0, t=0, pad=0),
        #                     template="simple_white")
        #         box_plt = plot(fig, output_type="div")
        #         box_plots.append(box_plt)
        # return box_plots       

    def get_scatterplot(self):
        df = self.read_df()
        num_col, cat_col, datetime_col = self.feature_segment()

        # scatter_plt = [feature for feature in num_col.columns if df[feature].nunique()/df.shape[0] >= 0.4]

        scatter_plt = list(combinations([feature for feature in num_col if df[feature].nunique()/df.shape[0] >= 0.4], 2))
        scatter_plots = []
        if len(scatter_plt) > 0:
            for cols in scatter_plt:
                fig = px.scatter(df, x=cols[0], y=cols[1], color=self.target_feature)
                fig.update_layout(
                            margin=dict(l=0, r=0, b=0, t=0, pad=0),
                            template="simple_white")
                scatter_plt = plot(fig, output_type="div")
                scatter_plots.append(scatter_plt)
        return scatter_plots



