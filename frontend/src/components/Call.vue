<template>
  <div>
    <SessionTopBar :timeLimit=time_limit timerCopy='Session ends in ' :sessionCopy=session_copy v-on:timer-expired="onTimerExpired"></SessionTopBar>
    <!---audio id="meditationbell" src='../assets/meditationbell.flac' muted></audio--->
    <a id='med-button' class='begin-meditation-button' v-on:click="unMuteButton()">Ready to meet your partner and start?</a>
    <audio id="meditationbell" src='https://ia800607.us.archive.org/28/items/LovelyMeditationBell/STE-015.flac' muted></audio>
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
      time_limit: 0,
    }
  },
  components: {
    SessionTopBar,
    SessionBottomBar,
    //VideoChat
  },
  props: {
    testSession: Boolean,
    roomName: String,
    medTime: Number
  },
  methods: {

    unMuteButton() {
      document.getElementById('meditationbell').muted = false;
      document.getElementById('med-button').style.display = 'none';;
      document.querySelector('iframe').style.visibility = "visible";
    },

    onTimerExpired() {

      if (this.debriefNext) { //set environment for debrief  

        //set noise for bell   
        //var audio = new Audio('../assets/meditationbell.flac')
        //var audio = new Audio('https://ia800607.us.archive.org/28/items/LovelyMeditationBell/STE-015.flac')
        //audio.play()
        //this.$refs.meditationbell.play();
        document.getElementById('meditationbell').play();
        //document.getElementById('meditationbell').muted = false;
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

    //set environment if test session 
    if (this.testSession) {
      this.session_copy = "Are your video and audio settings working?"
    }
    else { //set environment if meditation session
      this.debriefNext = true;
      console.log("med time is:",this.medTime);
      this.time_limit = (this.medTime > 0) ? this.medTime : 10 * 60;
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
      elem.style.width = "375px";
      elem.style.height = "750px";
      elem.style.right = "0em";
      elem.style.bottom = "0em";
      elem.style.visibility = "hidden";
    });
    dailycoScript.setAttribute('src', 'https://unpkg.com/@daily-co/daily-js/dist/daily-iframe.js');
    document.head.appendChild(dailycoScript);
  },

  watch: { //set page title
    $route: {
      immediate: true,
      handler(to, from) {
        document.title = (this.testSession) ? 'Test Room' : 'Meditation Room' || 'Some Default Title';
      }
    }
  },

  destroyed() {
    
    //delete vid chat
    var elem = document.querySelector('iframe');
    if (elem) {
      elem.style.display = 'none';
      callFrame.leave();
      callFrame.destroy();
    }
  }
}
</script>


<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1 {
  font-weight: normal;
}

.begin-meditation-button {
  font-size: 18px;
  font-family: 'DIN Condensed', sans-serif;
  border-radius: 5px;
  border: 2px solid #18A0FB;
  padding-top: 10px;
  padding-bottom: 10px;
  padding-right: 95px;
  padding-left: 95px;
  color: #18a0fb;
}

</style>
