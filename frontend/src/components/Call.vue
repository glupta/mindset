
<template>
  <div class='call'>
    <SessionTopBar :showTimer=show_timer :showBell=show_bell :showLeave=show_leave :timeLimit=time_limit :sessionCopy=session_copy @timer-expired="onTimerExpired" @bell-rings="bellRings" @leave-session="leaveSession"></SessionTopBar>
    <div class='med-button-wrapper'>
      <button id='med-button' class='get-started-button' @click='unMuteButton'>{{joinButtonCopy}}</button>
      <!--audio id="med-bell" src='https://ia800607.us.archive.org/28/items/LovelyMeditationBell/STE-015.flac' muted></audio-->
    </div>
    <!--audio id="med-bell" src='www.buddhanet.net/filelib/audio/tinsha.wav' type='audio/wav' muted crossOrigin="anonymous"></audio-->

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
      session_copy: '',
      show_timer: true,
      show_bell: true,
      show_leave: true,
      joinButtonCopy: ''
    }
  },
  components: {
    SessionTopBar,
    SessionBottomBar,
  },
  props: {
    testSession: Boolean,
    roomName: String,
    medTime: Number
  },
  methods: {

    unMuteButton() { //button clicked to start session
      
      //document.getElementById('med-bell').muted = false; //rule to override audio autoplay
      //this.audio = new Audio(require('../assets/meditationbell2.wav'));
      //this.med_bell = new Audio('http://www.buddhanet.net/filelib/audio/tinsha.wav');
      this.med_bell = new Audio(require('../assets/tinsha.wav'));
      this.med_bell.currentTime = 2;
      this.med_bell.addEventListener('canplaythrough', event => {
        console.log("audio loaded");
      });
      this.med_bell.muted = true;
      this.med_bell.play();
      //console.log("volume:",this.med_bell.volume);

      document.getElementById('med-button').style.display = 'none';
      
      document.querySelector('iframe').style.visibility = "visible"; //show vid chat

      this.show_leave = true;

      if (this.testSession) { //show copy at top for test session
        this.session_copy = "Test Video Chat & Bell"
        this.show_bell = true;
      }
      else { //show timer and copy at top for real session
        this.session_copy = "Say Hello, Begin Meditation";
        this.show_timer = true;
      }
    },

    bellRings() {

      //if (!this.med_bell) {
        //this.med_bell = new Audio('www.buddhanet.net/filelib/audio/tinsha.wav');
        //console.log("created audio");
      //}

      //var med_bell = document.getElementById('med-bell');
      //var med_bell = new Audio('www.buddhanet.net/filelib/audio/tinsha.wav');
      //if (!this.med_bell) {
        //this.med_bell = new Audio(require('../assets/tinsha.wav'));
      //  console.log("bell does not exist");
      //}

      //var med_bell = this.med_bell;

      if (!this.med_bell.paused) {
        this.med_bell.pause();
        this.med_bell.currentTime = 2;
        console.log("audio paused");
      }

      this.med_bell.muted = false;
      this.med_bell.volume = 1;

      //med_bell.addEventListener('canplaythrough', event => {
        var play_promise = this.med_bell.play();
        if (play_promise !== undefined) {
          play_promise.then(function() {
            console.log("audio played");
          }).catch(function(error) {
            console.log("audio error:",error);

            //if (!this.med_bell2) {
              //var med_bell2 = new Audio(require('../assets/tinsha.wav'));
              //med_bell.setAttribute('src','../assets/tinsha.wav')
            //}

          // if (!this.med_bell.paused) {
          //   this.med_bell.pause();
          //   console.log("audio paused");
          // }

          // med_bell2.load();
          // med_bell2.muted = false;
          // med_bell2.volume = 1;
          // med_bell2.play();
          });
        }
      //});
    },

    leaveSession() {
      if (this.testSession) {
        router.push({ name: 'WaitingRoom' });
      }
      else {
        router.push({ name: 'SessionEnd' });
      }
    },

    onTimerExpired() {

      if (this.debriefNext) { //set environment for debrief  

        //play ending bell
        //document.getElementById('meditationbell').play();
        this.bellRings();
        
        //set debrief environment
        this.debriefNext = false;
        this.time_limit = 2 * 60;
        this.session_copy = "Thank Your Partner. Good Bye!";
        this.show_timer = false;
      }
      else { //if debrief ended
        router.push({ name: "SessionEnd" });
      }
    },

    killVidChat() {
      var elem = document.querySelector('iframe');
      if (elem) {
        elem.style.display = 'none';
        callFrame.leave();
        callFrame.destroy();
        console.log("killed vid chat");
      }
      else {
        console.log("did not find vid chat");
      }
    }
  },

  mounted() {

    this.killVidChat();

    if (!this.roomName) { //kick out if room name not given
      router.push({ name: "SessionEnd" });
      return;
    }

    //hide timer & leave button to start with
    this.show_timer = false;
    this.show_bell = false;
    this.show_leave = false;

    //this.med_bell = new Audio();
    //this.med_bell2 = new Audio();

    //set environment if test session 
    if (this.testSession) {
      //this.session_copy = "Are your video and audio settings working?";
      console.log("test session");
      this.joinButtonCopy = 'Enter Test Room';
    }
    else { //set environment if meditation session
      this.debriefNext = true;
      console.log("med time is:",this.medTime);
      this.time_limit = (this.medTime > 0) ? this.medTime : 15 * 60;
      //this.session_copy = "Please begin meditation";
      this.joinButtonCopy = 'Enter Meditation Room';
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

  beforeDestroy() {
    
    //delete vid chat
    this.killVidChat();

    //stop bell rings
    if (this.med_bell) this.med_bell.pause();
  }
}
</script>


<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1 {
  font-weight: normal;
}

.med-button-wrapper {

  align-items: center;
  justify-content: center;
  display: flex;

  height: 358px;
}

.get-started-button {
  background-color: #2AD9FF;
  border: 1px solid #2AD9FF;
  box-sizing: border-box;
  border-radius: 6px;
  color: #FFFFFF;
  font-size: 24px;

  width: 271px;
  height: 58px;



/*
  margin:0 auto;
  display:block;

  line-height: 22px;
  padding-top: 18px;
  padding-bottom: 20px;
  padding-right: 40px;
  padding-left: 40px;

  margin: 0;
  position: absolute;
  top: 50%;
  left: 50%;
*/

  box-sizing: border-box;
  cursor:pointer;
}

.iframe-container {
  margin-top: 50px;
}

</style>
