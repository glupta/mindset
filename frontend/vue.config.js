const path = require('path');

module.exports = {
  css: {
    loaderOptions: {
      sass: {
        data: `@import "@/stylesheet.scss";`
      }
    }
  }
};