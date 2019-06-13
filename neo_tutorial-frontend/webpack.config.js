const path = require('path');

// const CleanWebpackPlugin = require('clean-webpack-plugin');
// const HtmlWebpackPlugin = require('html-webpack-plugin');

const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const TerserPlugin = require('terser-webpack-plugin');
var CopyWebpackPlugin = require('copy-webpack-plugin');

module.exports = {

    mode: 'production',
    devtool: 'source-map',

    optimization: {
        minimizer: [new TerserPlugin()],
    },

    entry: [
        './node_modules/angular',
        './js/main.js', './js/admin.js', './js/portal.js',
        './scss/style.scss'
    ],
    output: {
        filename: '[name].js',
        path: __dirname + '/dist'
    },

    module: {
        rules: [
            {
                test: /\.scss$/,
                use: [
                    MiniCssExtractPlugin.loader,
                    "css-loader",
                    "sass-loader"
                ]
            },
            {
                test: /\.js$/,
                use: [
                    {
                        loader: 'babel-loader'
                    }
                ]
            }
        ]
    },
    plugins: [
        new MiniCssExtractPlugin({
            // Options similar to the same options in webpackOptions.output
            // both options are optional
            filename: "[name].css",
            chunkFilename: "[id].css"
        }),
        new CopyWebpackPlugin([
            {from:'./images',to: 'images'}
        ])
        // new CleanWebpackPlugin(),
        // new HtmlWebpackPlugin({
        //     title: 'Production'
        // })
    ]
};



