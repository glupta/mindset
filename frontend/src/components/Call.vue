<template>
  <div class='call'>
    <SessionTopBar :timeLimit=time_limit timerCopy='Session ends in ' :sessionCopy=session_copy @timer-expired="onTimerExpired"></SessionTopBar>

    <button id='med-button' class='get-started-button' @click='unMuteButton()'>Click here to start</button>
    <audio id="meditationbell" src='https://ia800607.us.archive.org/28/items/LovelyMeditationBell/STE-015.flac' muted></audio>
    
    <!--SessionBottomBar></SessionBottomBar-->
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
      time_limit: 0,
      session_copy: ''
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
      document.getElementById('med-button').style.display = 'none';
      document.querySelector('iframe').style.visibility = "visible";
      this.session_copy = (this.testSession) ? "Audio/video settings working?" : "Say hi & begin meditation";
    },

    onTimerExpired() {

      if (this.debriefNext) { //set environment for debrief  

        //play ending bell
        document.getElementById('meditationbell').play();
         
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
      //this.session_copy = "Are your video and audio settings working?";
      console.log("test session");
    }
    else { //set environment if meditation session
      this.debriefNext = true;
      console.log("med time is:",this.medTime);
      this.time_limit = (this.medTime > 0) ? this.medTime : 10 * 60;
      //this.session_copy = "Please begin meditation";
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
      elem.style.width = "100%";
      elem.style.height = "90%";
      //elem.style.height = "100%";
      //elem.style.margin = "10px";
      //elem.style.right = "-10px";
      //elem.style.bottom = "-10px";
      //elem.style.left = "-10px";
      //elem.style.top = "-10px";
      //elem.style.bottom = "auto";     
      //elem.style.width = "375px";
      //elem.style.height = "750px";
      elem.style.top = "50px";
      elem.style.right = "0em";
      elem.style.bottom = "0em";
      //elem.style.bottom = "10px";
      elem.style.visibility = "hidden";
      //elem.style.overflow = "scroll";
      //elem.style.display = 'none';
    });
    dailycoScript.setAttribute('src', 'https://unpkg.com/@daily-co/daily-js/dist/daily-iframe.js');
    dailycoScript.setAttribute('crossorigin','');
    dailycoScript.setAttribute('allowfullscreen',true);
    document.body.appendChild(dailycoScript);
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

.call {
  position: relative;
  height: 200px;
}

.get-started-button {
  background-color: #2AD9FF;
  border: 1px solid #2AD9FF;
  box-sizing: border-box;
  border-radius: 6px;
  color: #FFFFFF;
  font-size: 24px;
/*
  width: 271px;
  line-height: 22px;
  height: 58px;

  margin: 0;
  position: absolute;
  top: 50%;
  left: 50%;
*/

  padding-top: 20px;
  padding-bottom: 20px;
  padding-right: 40px;
  padding-left: 40px;
}

.iframe-container {
  margin-top: 50px;
}

</style>
