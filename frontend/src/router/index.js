import Vue from 'vue'
import Router from 'vue-router'
import Home4 from '@/components/Home4'
import SignUp from '@/components/SignUp'
import SignUpHabit from '@/components/SignUpHabit'
import HomeSelfInfo from '@/components/HomeSelfInfo'
import VueCookies from 'vue-cookies';

Vue.use(Router)
Vue.use(VueCookies);

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      name: 'Home4',
      component: Home4
    },
    {
      path: '/signup',
      name: 'SignUp',
      component: SignUp
    },
    {
      path: '/newhabit',
      name: 'SignUpHabit',
      component: SignUpHabit
    },
    {
      path: '/dashboard',
      name: 'HomeSelfInfo',
      component: HomeSelfInfo
    },
  ]
})
