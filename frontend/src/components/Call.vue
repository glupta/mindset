
<template>
  <div class='call'>
    <SessionTopBar :showTimer=show_timer :leftCopy=left_copy :showLeave=show_leave :timeLimit=time_limit :sessionCopy=session_copy @timer-expired="onTimerExpired" @left-action="startTimer" @leave-session="leaveSession"></SessionTopBar>
    <div class='load-wrapper' id='load-wrapper'>
      <!--button id='med-button' class='get-started-button' @click='unHideButton'>{{joinButtonCopy}}</button-->
      <p>
        Connecting in...
        <br><br>
        <Timer :timeLimit='time_start' @timer-expired='onLoadTimerExpired'>
      </p>
    </div>
    <div class='load-input' id='load-input'>
      <p>
        Duration of session timer?
        <br><br>
        <input v-model='med_input' placeholder='Enter in seconds'>
        <button @click='inputMedTime'>Submit</button>
      </p>
    </div>
    <!--SessionBottomBar></SessionBottomBar-->
  </div>
</template>

<script>
import SessionTopBar from '@/components/SessionTopBar'
import SessionBottomBar from '@/components/SessionBottomBar'
import Timer from '@/components/Timer'
import router from '../router'
export default {
  name: "Call",
  data () {
    return {
      time_limit: 0,
      session_copy: '',
      left_copy: ' ',
      show_timer: true,
      show_leave: true,
      chat_height: 0,
      //med_input: 0
      //joinButtonCopy: ''
    }
  },
  components: {
    SessionTopBar,
    SessionBottomBar,
    Timer
  },
  props: {
    testSession: Boolean,
    roomName: String,
    medTime: Number
  },

  mounted() {

    // var link = document.createElement('link');
    // link.rel = 'icon';
    // link.href = 'https://www.dropbox.com/s/wal7owvpfnsz1s8/ak93l-iosff-003.png';
    // document.getElementsByTagName('head')[0].appendChild(link);

    this.killVidChat(); //delete any loose iframe

    if (!this.roomName) { //kick out if room name not given
      router.push({ name: "SessionEnd" });
      return;
    }

    //hide everything to start with
    this.show_timer = false;
    //this.show_left = false;
    //this.show_leave = false;
    this.show_leave = false;
    this.left_copy = '';

    this.sessionStatus = 'load'; //show loading page

    if (this.testSession) {
      document.getElementById('load-wrapper').style.display = 'none';
    }
    else {
      document.getElementById('load-input').style.display = 'none';
      this.time_start = 9;
    }

    //call daily.co API to add user to assigned video chat room
    var room_url = "https://meditate-live.daily.co/";
    room_url += String(this.roomName);
    console.log("call is mounted, room url:",room_url);
    let dailycoScript = document.createElement('script');
    dailycoScript.addEventListener("load", event => {
      window.callFrame = window.DailyIframe.createFrame();
      callFrame.join({ url: room_url});
      var elem = document.querySelector('iframe');
      elem.style.position = "absolute";
      elem.style.top = "50px";
      elem.style.right = "0";
      elem.style.width = "100%";
      elem.style.height = "calc(100% - 50px)";
      //this.chat_height = window.innerHeight - 50;
      //elem.style.height = this.chat_height + 'px';
      elem.style.visibility = "hidden";

      //window.addEventListener('resize',this.chatResize);
      // window.addEventListener('resize', event => {
      //   this.chat_height = window.innerHeight - 50;
      //   elem.style.height = this.chat_height + 'px';
      //   console.log('height:',this.chat_height);
      // });
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

    //stop bell ring
    if (this.med_bell) {
      this.med_bell.pause();
      console.log('bell paused at exit');
    }
  },

  Destroyed() {
    //delete vid chat
    this.killVidChat();
  },

  methods: {

    // unHideButton() { //button clicked to start session
      
    //   //load audio file, overcome autoplay issue
    //   this.med_bell = new Audio(require('@/assets/meditationbell.mp3'));
    //   this.med_bell.addEventListener('canplaythrough', event => {
    //     console.log("audio loaded");
    //   });

    //   //workaround to loop audio on mute
    //   this.med_bell.muted = true;
    //   this.med_bell.loop = true;
    //   this.med_bell.play();

    //   //hide button and show vid chat environment
    //   document.getElementById('load-wrapper').style.display = 'none';
    //   document.querySelector('iframe').style.visibility = "visible";
    //   this.show_leave = true;

    //   if (this.testSession) { //show bell and copy at top for test session
    //     this.session_copy = "Test Video Chat & Bell Volume";
    //     this.left_copy = "Bell";
    //   }
    //   else { //show timer and copy at top for real session
    //     this.session_copy = "Say Hello & Begin Meditation";
    //     this.show_timer = true;
    //     this.left_copy = "Timer";
    //   }
    // },

    inputMedTime() { //input meditation time for test session
      
      if (!isNaN(parseInt(this.med_input)) && this.med_input > 0) {
        document.getElementById('load-input').style.display = 'none';
        this.session_copy = 'Check Settings & Start Timer';
        this.startSession();  
      }
    },

    startTimer() { //timer starts when button clicked

      //load audio file, overcome autoplay issue
      if (!this.med_bell) {
        this.med_bell = new Audio(require('@/assets/meditationbell.mp3'));
        console.log('new audio');
      }
        
      // if (this.testSession) {
      //   this.bellRings();
      // }
      // else {

      //workaround to loop audio on mute
      this.med_bell.muted = true;
      this.med_bell.loop = true;
      this.med_bell.play();

      this.left_copy = '';
      this.show_timer = true;
      this.session_copy = "Please Begin Meditation";

      if (this.testSession) {
        this.time_limit = (this.med_input > 0) ? this.med_input : 15 * 60;
      }
      else {
        console.log("med time is:",this.medTime);
        this.time_limit = (this.medTime > 0) ? this.medTime : 15 * 60;
      }
    },

    bellRings() { //bell rings after timer expires

      //reset and unmute audio
      console.log("audio played");
      this.med_bell.currentTime = 0;
      this.med_bell.muted = false;
      this.med_bell.volume = 1;
      this.med_bell.loop = false;

      this.med_bell.addEventListener('canplaythrough', event => {
        console.log("audio loaded");
      });

      // if (!this.med_bell.paused) {
      //   this.med_bell.pause();
      // }

      this.med_bell.play();
    },

    //if test session, take user to waiting room. otherwise, session end page.
    leaveSession() {
      if (this.testSession) {
        router.push({ name: 'WaitingRoom' });
      }
      else {
        router.push({ name: 'SessionEnd' });
      }
    },

    onLoadTimerExpired() { //load timer triggers this which redirects to main expire function
      this.onTimerExpired();
    },

    onTimerExpired() { //function runs based on stage of session when timer expires

      if (this.sessionStatus == 'load') {

        document.getElementById('load-wrapper').style.display = 'none';
        this.session_copy = 'Say Hello & Start Timer';
        // document.querySelector('iframe').style.visibility = "visible";
        // this.sessionStatus = 'meditate';
        // this.show_leave = true;

        // //set environment if test session 
        // if (this.testSession) {
        //   //this.session_copy = "Are your video and audio settings working?";
        //   console.log("test session");
        //   //this.joinButtonCopy = 'Enter Test Room';
        //   this.session_copy = "Test Video Chat & Bell";
        //   this.left_copy = "Bell";

        // }
        // else { //set environment if meditation session
        //   console.log("med time is:",this.medTime);
        //   //this.time_limit = (this.medTime > 0) ? this.medTime : 15 * 60;
        //   //this.session_copy = "Please begin meditation";
        //   //this.joinButtonCopy = 'Enter Meditation Room';
        //   this.left_copy = "Start";
        //   this.session_copy = 'Say Hello & Start Timer';
        // }

        this.startSession();

      }
      else if (this.sessionStatus == 'meditate') { //set environment for debrief  
        
        //set debrief environment
        this.sessionStatus = 'debrief';
        this.time_limit = 5 * 60;
        this.show_timer = false;

        this.session_copy = (this.testSession) ? "Session Complete. Good Bye!" : "Thank Your Partner. Good Bye!";

        //play ending bell
        this.bellRings();
      }
      else if (this.sessionStatus == 'debrief') { //if debrief ended
        router.push({ name: "SessionEnd" });
      }
      else {
        console.log("session status error");
        return;
      }
    },


    startSession() { //set meditate environment

      //document.body.style.zoom = 1.0;
      //this.blur();
      //document.body.style.transform = 'scale(' + 1.0 + ')'; // set zoom
      //document.body.style.transformOrigin = '50% 0'; // set transform scale base

      document.querySelector('iframe').style.visibility = "visible";
      this.sessionStatus = 'meditate';
      this.show_leave = true;
      this.left_copy = "Start";
    },

    //disconnect from vid chat & delete iframe
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
  }
}
</script>


<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1 {
  font-weight: normal;
}

.load-wrapper {

  align-items: center;
  justify-content: center;
  display: flex;
  height: 358px;
  font-size: 36px;
}

.load-input {

  align-items: center;
  justify-content: center;
  display: flex;
  height: 358px;
  font-size: 24px;
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

  box-sizing: border-box;
  cursor:pointer;
}

</style>
