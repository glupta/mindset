import Vue from 'vue'
import Router from 'vue-router'
import Home from '@/components/Home'
import ScheduleSession from '@/components/ScheduleSession'
import ScheduleSession2 from '@/components/ScheduleSession2'
import ScheduleSession3 from '@/components/ScheduleSession3'
import ScheduleSession4 from '@/components/ScheduleSession4'
import ScheduleSession5 from '@/components/ScheduleSession5'
import ScheduleSessionOL from '@/components/ScheduleSessionOL'
import FullscreenTest from '@/components/FullscreenTest'
import ScheduleSessionNew from '@/components/ScheduleSessionNew'
import ScheduleConfirmation from '@/components/ScheduleConfirmation'
import SessionEnd from '@/components/SessionEnd'
import WaitingRoom from '@/components/WaitingRoom'
import Call from '@/components/Call'
import Test from '@/components/Test'
import SessionLanding from '@/components/SessionLanding'
import VueCookies from 'vue-cookies';
import NoSleep from 'nosleep.js';
import moment from 'moment';
import '@/assets/css/reset.css'
//import stylesheet from '@/stylesheet.scss';
//import '@/assets/css/schedulePublicSession.css'
//import '@/assets/css/scheduleNewSession.css'
//import '@/assets/css/scheduleNewSessionPopUp.css'

Vue.use(Router)
Vue.use(VueCookies);

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      name: 'Home',
      component: Home
    },
    {
      path: '/plan',
      name: 'ScheduleSession',
      component: ScheduleSession
    },
    {
      path: '/public',
      name: 'ScheduleSession2',
      component: ScheduleSession2
    },
    {
      path: '/plan3',
      name: 'ScheduleSession3',
      component: ScheduleSession3
    },
    {
      path: '/plan4',
      name: 'ScheduleSession4',
      component: ScheduleSession4
    },
    {
      path: '/plan5',
      name: 'ScheduleSession5',
      component: ScheduleSession5
    },
    {
      path: '/ol',
      name: 'ScheduleSessionOL',
      component: ScheduleSessionOL
    },
    {
      path: '/full',
      name: 'FullscreenTest',
      component: FullscreenTest
    },
    {
      path: '/new',
      name: 'ScheduleSessionNew',
      component: ScheduleSessionNew
    },
    {
      path: '/confirm',
      name: 'ScheduleConfirmation',
      component: ScheduleConfirmation
    },
    {
      path: '/wait',
      name: 'WaitingRoom',
      component: WaitingRoom
    },
    {
      path: '/end',
      name: 'SessionEnd',
      component: SessionEnd
    },
    {
      path: '/call',
      name: 'Call',
      component: Call,
      props: true
    },
    {
      path: '/test',
      name: 'Test',
      component: Test,
      props: true
    },
    {
      path: '/sessionLanding',
      name: 'SessionLanding',
      component: SessionLanding
    }
  ]
})
