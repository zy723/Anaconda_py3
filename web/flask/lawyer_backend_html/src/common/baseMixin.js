

export default {
  data() {
    return {

    }
  },

  methods: {
    
    getStrleng(str, max) {
      var myLen = 0
      for (var i = 0; i < str.length && myLen <= max * 2; i++) {
        if (str.charCodeAt(i) > 0 && str.charCodeAt(i) < 128) {
          myLen++
        } else myLen += 2
      }
      return myLen
    }
  }
}
