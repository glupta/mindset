<template>
  <div>
    <SessionTopBar :timeLimit='10 * 60' timerCopy='Session ends in ' v-on:timer-expired="onTimerExpired"></SessionTopBar>
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

    dailycoScript.addEventListener("load", function(event) {
      window.callFrame = window.DailyIframe.createFrame();
      callFrame.join({ url: 'https://meditation-hub.daily.co/hello' });
      var elem = document.querySelector('iframe');
      elem.style.width= "375px";
      elem.style.height = "750px";
      elem.style.right= "0em";
      elem.style.bottom= "0em";
    });

    dailycoScript.setAttribute('src', 'https://unpkg.com/@daily-co/daily-js/dist/daily-iframe.js')
    document.head.appendChild(dailycoScript)
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1 {
  font-weight: normal;
}
</style>
