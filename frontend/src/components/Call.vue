<template>
  <div>
    <SessionTopBar timerCopy='Session ends in ' v-on:timer-expired="onTimerExpired"></SessionTopBar>
    <p>Bowenn</p>
    <SessionBottomBar></SessionBottomBar>
  </div>
</template>

<script>
import SessionTopBar from '@/components/SessionTopBar'
import SessionBottomBar from '@/components/SessionBottomBar'
import router from '../router'
export default {
  name: "Call",
  components: {
    SessionTopBar,
    SessionBottomBar
  },
  props: [
    'testSession'
  ],
  methods: {
    onTimerExpired() {
      router.push({ name: "SessionEnd" })
    }
  },
  mounted () {
    let dailycoScript = document.createElement('script')
    dailycoScript.setAttribute('src', 'https://unpkg.com/@daily-co/daily-js@0.9.988/dist/daily-iframe.js')
    document.head.appendChild(dailycoScript)

    window.addEventListener("load", function(event) {
      //console.log('fired')
      //let myRoom = this.createMtgRoom()
      //console.log(myRoom)

      window.callFrame = window.DailyIframe.createFrame();
      callFrame.join({ url: 'https://meditation-hub.daily.co/hello' });
    });

    //console.log('akal wettakal')
  }/*,
  methods: {
    createMtgRoom: function () {
      let room = {
        "id":"e59809f1-e025-46cf-ac4e-3ddf38f6d66b",
        "name":"hello",
        "api_created":false,
        "privacy":"public",
        "url":"https://meditation-hub.daily.co/hello",
        "created_at":"2020-05-02T16:47:13.000Z",
        "dialInPIN":"930940",
        "config":{}
      }
      return room;
	  }
  }*/
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1 {
  font-weight: normal;
}
</style>
