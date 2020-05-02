import Vue from 'vue'
import Router from 'vue-router'
import Home from '@/components/Home'
import Call from '@/components/Call'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Home',
      component: Home
    },
    {
      path: '/call',
      name: 'Call',
      component: Call
    }
  ]
})
