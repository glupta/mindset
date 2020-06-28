<template>
  <div>
    <SessionTopBar :timeLimit=time_limit timerCopy='Session ends in ' :sessionCopy=session_copy v-on:timer-expired="onTimerExpired"></SessionTopBar>
    <SessionBottomBar></SessionBottomBar>
  </div>
</template>

<script>
import SessionTopBar from '@/components/SessionTopBar'
import SessionBottomBar from '@/components/SessionBottomBar'
//import VideoChat from '@/components/VideoChat'
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
    SessionBottomBar,
    //VideoChat
  },
  props: {
    testSession: Boolean,
    roomName: String
  },
  methods: {

    onTimerExpired() {

      if (this.testSession) //do not reroute if test session
        return;

      if (this.debriefNext) { //set environment for debrief
      
        this.debriefNext = false;
        this.time_limit = 2 * 60;
        this.session_copy = "How was your session?";
      }
      else { //if debrief ended
        router.push({ name: "SessionEnd" });
      }
    }
  },

  mounted() {


    if (!this.roomName) { //kick out if room name not given
      router.push({ name: "SessionEnd" });
      return;
    }

    //set environment if not test session 
    if (!this.testSession) {
      this.debriefNext = true;
      this.time_limit = 10 * 60;
      this.session_copy = "Please begin meditation";
    }

    //call daily.co API to add user to assigned video chat room
    var room_url = "https://meditate-live.daily.co/";
    room_url += String(this.roomName);
    console.log("call is mounted, room url:",room_url);
    let dailycoScript = document.createElement('script');
    dailycoScript.addEventListener("load", function(event) {
      window.callFrame = window.DailyIframe.createFrame();
      callFrame.join({ url: room_url});
      var elem = document.querySelector('iframe');
      elem.style.width= "375px";
      elem.style.height = "750px";
      elem.style.right= "0em";
      elem.style.bottom= "0em";
    });
    dailycoScript.setAttribute('src', 'https://unpkg.com/@daily-co/daily-js/dist/daily-iframe.js');
    document.head.appendChild(dailycoScript);
  },

  watch: { //set page title
    $route: {
      immediate: true,
      handler(to, from) {
        let page_title = 'Meditation Room';
        if (this.testSession)
          page_title = 'Test Room';
        document.title = page_title || 'Some Default Title';
      }
    }
  },

  destroyed() {
    
    //remove user from active_users table
    var elem = document.querySelector('iframe');
    if (elem) {
      elem.style.display = 'none';
      callFrame.leave();
      callFrame.destroy();
      //delete vid chat room as well
    }
  }
}
</script>


<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1 {
  font-weight: normal;
}
</style>
