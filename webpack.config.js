const path = require('path');

module.exports = {
  entry: {
    app: './src/index.ts'
  },

  module: {
    rules: [{
      test: /\.tsx?$/, 
      use: 'ts-loader',  
      exclude: /node_modules/, 
      
    }]
  },
  watch: true,
  resolve: {
    extensions: ['.tsx', '.ts', '.js']
  },
  watch: true,
  
  output: {
    filename: 'bundle.min.js',
    path: path.resolve(__dirname, 'static/js/dist')
  },

};