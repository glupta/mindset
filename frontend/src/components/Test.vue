
<template>
  <div class='call'>
    <SessionTopBar :showTimer=show_timer :showLeft=show_left :leftCopy=left_copy :showLeave=show_leave :timeLimit=time_limit :sessionCopy=session_copy @timer-expired="onTimerExpired" @left-action="startTimer" @leave-session="leaveSession"></SessionTopBar>
  </div>
</template>

<script>
import SessionTopBar from '@/components/SessionTopBar'
import router from '../router'
export default {
  name: "Test",
  data () {
    return {
      time_limit: 0,
      session_copy: '',
      left_copy: '',
      show_timer: true,
      show_leave: true,
      show_left: true,
      DAILYID: 'meditate' //use meditate or meditatelive
    }
  },
  components: {
    SessionTopBar
  },
  props: {
    roomName: String
  },

  mounted() {

    this.killVidChat(); //delete any loose iframe
    document.body.style.backgroundColor = "#FFFFFF";

    this.show_timer = false;
    this.show_left = true;
    this.left_copy = 'START';
    this.show_leave = true;
    this.session_copy = "Press START when you appear at the bottom";
    this.time_limit = 60;
    this.timer_kick = true;

    if (this.roomName) { //connect if room name given
      this.room_name = this.roomName;
    }
    else if (this.$cookies.isKey('medliveorg')) { //use cookie to find room
        this.room_name = this.$cookies.get('medliveorg');
        console.log(this.client_id,": found cookie");
    }
    else { //create cookie if not found
        this.room_name = Math.random().toString(36).slice(-5);
        this.$cookies.set('medliveorg',this.client_id,-1);
        console.log("create cookie");
    }

    var entry = {
        room_name: this.room_name
      };

    fetch('/api/roomtoken', { //call backend to get room data
    method: "POST",
    body: JSON.stringify(entry),
      headers: new Headers({
      "content-type": "application/json"
      })
    })
    .then(response => {
      if (response.status !== 200) { //server error handling
        console.log(`Looks like there was a problem. Status code: ${response.status}`);
        return;
      }
      response.json().then(data => { //info about client added to active users in DB
        //console.log("data: ",data);

        if ('error' in data) { //error handling from testroom backend call
          console.log(this.client_id,": roomtoken error: ",data['error']);
          alert("roomtoken error: " + data['error']);
          return;
        }

        //take token from backend call
        if ('token' in data) {
          //console.log("token: ",data['token']);
          
          //call daily.co API to add user to assigned video chat room
          var room_url = "https://" + this.DAILYID + ".daily.co/" + this.room_name + "?t=" + data['token'];
          //console.log(this.room_name,", call is mounted, room url:",room_url);
          let dailycoScript = document.createElement('script');
          dailycoScript.addEventListener("load", event => {
            window.callFrame = window.DailyIframe.createFrame({showFullscreenButton: true});
            callFrame.join({ url: room_url});
            var elem = document.querySelector('iframe');
            elem.style.position = "absolute";
            elem.style.top = "50px";
            elem.style.right = "0";
            elem.style.width = "100%";
            elem.style.height = "calc(100% - 50px)";
            elem.style.visibility = "visible";
          });
          dailycoScript.setAttribute('src', 'https://unpkg.com/@daily-co/daily-js/dist/daily-iframe.js');
          dailycoScript.setAttribute('crossorigin','');
          dailycoScript.setAttribute('allowfullscreen',true);
          document.body.appendChild(dailycoScript);
        }
        else {
          alert("token data missing");
          return;
        }
      });
    })
    .catch(error => { //error handling
      console.log("Fetch error: " + error);
    });
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

  watch: { //set page title
    $route: {
      immediate: true,
      handler(to, from) {
        document.title = (this.test_session) ? 'Test Room' : 'Meditation Room' || 'Some Default Title';
      }
    }
  },

  methods: {

    startTimer() { //timer starts when button clicked

      this.timer_kick = false;
      this.time_limit = 10;

      //load audio file, overcome autoplay issue
      if (!this.med_bell) {
        this.med_bell = new Audio(require('@/assets/meditationbell.mp3'));
        //console.log('new audio');
      }

      //workaround to loop audio on mute
      this.med_bell.muted = true;
      this.med_bell.loop = true;
      this.med_bell.play();

      //this.show_left = false;
      this.left_copy = '';
      this.show_timer = true;
      this.session_copy = "Let the timer run out";

      setTimeout(() => this.session_copy = 'Sessions last 15 minutes',5000);
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

      this.med_bell.play();
    },

    //if test session, take user to waiting room. otherwise, session end page.
    leaveSession() {
      console.log("kick out");
      router.push({ name: 'WaitingRoom' });
    },

    onTimerExpired() { //function runs based on stage of session when timer expires

      if (this.timer_kick) { //kicks out if user inactive for 30 sec
        this.leaveSession();
      }
      else { //set environment for debrief  
        
        //set debrief environment
        this.timer_kick = true;
        this.time_limit = 11;
        this.show_timer = false;
        this.show_left = false;
        this.session_copy = "Did the bell ring? Press LEAVE to exit";

        //play ending bell
        this.bellRings();
      }
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

</style>
