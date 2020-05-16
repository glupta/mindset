<template>
  <div>
    <SessionTopBar :timeLimit=time_limit timerCopy='Session ends in ' :sessionCopy=session_copy v-on:timer-expired="onTimerExpired"></SessionTopBar>
    <SessionBottomBar></SessionBottomBar>
  </div>
</template>

<script>
import SessionTopBar from '@/components/SessionTopBar'
import SessionBottomBar from '@/components/SessionBottomBar'
import router from '../router'
export default {
  name: "Call",
  data () {
    return {
      time_limit: 0
    }
  },
  components: {
    SessionTopBar,
    SessionBottomBar
  },
  props: [
    'testSession'
  ],
  methods: {

    onTimerExpired() {
      if (this.debriefNext) {
        this.debriefNext = false;
        this.time_limit = 2 * 60;
        this.session_copy = "How was your session?";
      } else {
        router.push({ name: "SessionEnd" });
      }
    }
  },
  mounted() {
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

    this.debriefNext = true;
    this.time_limit = 1 * 60;
    this.session_copy = "Please begin meditation";

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
