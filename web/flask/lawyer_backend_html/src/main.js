import Vue from 'vue'
import App from './App'

import pageHead from './components/uni-nav-bar/uni-nav-bar.vue'
import pageFoot from './components/page-foot.vue'
import uLink from '@/components/uLink.vue'
import request from './common/request.js'
import api from './api/index.js'
import url from './common/config.js'
import store from './store'
import './static/style/reset.css'
Vue.config.productionTip = false
Vue.prototype.$request = request
Vue.prototype.$api = api
Vue.prototype.$url = url
Vue.prototype.$store = store
Vue.prototype.$backgroundAudioData = {
	playing: false,
	playTime: 0,
	formatedPlayTime: '00:00:00'
}

Vue.component('page-head', pageHead)
Vue.component('page-foot', pageFoot)
Vue.component('uLink', uLink)

App.mpType = 'app'

const app = new Vue({
	store,
	...App
})
app.$mount()

