
<template>
  <div class='call'>
    <SessionTopBar :showTimer=show_timer :showLeft=show_left :leftCopy=left_copy :showLeave=show_leave :timeLimit=time_limit :sessionCopy=session_copy @timer-expired="onTimerExpired" @left-action="startTimer" @leave-session="leaveSession"></SessionTopBar>
    <div class='load-wrapper' id='load-wrapper'>
      <p>
        Connecting...
        <br><br>
        <Timer :timeLimit='time_start' @timer-expired='onLoadTimerExpired'>
      </p>
    </div>
</template>

<script>
import SessionTopBar from '@/components/SessionTopBar'
import Timer from '@/components/Timer'
import router from '../router'
export default {
  name: "Call",
  data () {
    return {
      time_limit: 0,
      session_copy: '',
      left_copy: '',
      show_timer: true,
      show_left: true,
      show_leave: true,
      DAILYID: 'meditate' //use meditate or meditatelive
    }
  },
  components: {
    SessionTopBar,
    Timer
  },
  props: {
    clientID: String,
    roomName: String,
    medTime: Number,
    skipStart: Number
  },

  mounted() {

    this.killVidChat(); //delete any loose iframe
    document.body.style.backgroundColor = "#FFFFFF";
    //this.show_left = false;
    this.session_kick = true;

    document.getElementById('load-wrapper').style.display = 'none';
    this.session_copy = 'Say hello to each other';
    this.show_timer = false;
    this.left_copy = "START";

    if (this.clientID && this.roomName) { //connect if client ID & room name given

      this.client_id = this.clientID;
      this.room_name = this.roomName;
      
      //hide everything to start with
      //this.show_timer = false;
      //this.show_leave = false;
      //this.time_start = 9; //load time
      this.time_limit = 5 * 60; 
      this.sessionLoad();
    }
    else if (this.$cookies.isKey('medliveorg')) { //use cookie to find room

      //reset session environment 
      document.getElementById('load-wrapper').style.display = 'none';
      this.session_copy = 'Connection lost, timer stopped.';
      this.time_limit = 20 * 60; 

      this.client_id = this.$cookies.get('medliveorg');
      console.log(this.client_id,": found cookie");

      this.checkRoom(true); //get room data and load session
    }
    else { //kick user out if no cookie
      console.log("no cookie, kick out");
      router.push({ name: "SessionEnd" });
      return;
    }
  },

  watch: { //set page title
    $route: {
      immediate: true,
      handler(to, from) {
        document.title = (this.test_session) ? 'Test Room' : 'Meditation Room' || 'Some Default Title';
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

    checkRoom(load_bool) { //call backend to get room data
      fetch('/api/checkroom?clientID=' + this.client_id)
      .then(response => {
        if (response.status !== 200) { //server error handling
          console.log(`Looks like there was a problem. Status code: ${response.status}`);
          return;
        }
        response.json().then(data => { //info about client added to active users in DB
          //console.log("data: ",data);

          if ('error' in data) { //error handling from testroom backend call
            console.log(this.client_id,": checkroom error: ",data['error']);
            alert("checkroom error: " + data['error']);
            return;
          }

          //take room name from backend call
          if ('room_name' in data) { 
            this.room_name = String(data['room_name']);
            //console.log(this.client_id,": room name: ",this.room_name);
          }
          else {
            alert("room data missing");
            return;
          }
          if (load_bool) this.sessionLoad(); //load session if requested
        });
      })
      .catch(error => { //error handling
        console.log("Fetch error: " + error);
      });
    },

    sessionLoad() { //load video chat with room name

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
              //elem.style.visibility = (this.roomName) ? "hidden" : "visible";
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

    startTimer() { //timer starts when both users press START

      this.session_kick = false;
      this.show_left = false;

      //load audio file, overcome autoplay issue
      if (!this.med_bell) {
        this.med_bell = new Audio(require('@/assets/meditationbell.mp3'));
        //console.log('new audio');
      }

      //workaround to loop audio on mute
      this.med_bell.muted = true;
      this.med_bell.loop = true;
      this.med_bell.play();

      if (this.skipStart > 0) { //query given d=1, then skip
        this.beginMeditation();
      }
      else { //start with partner

        //let user know to wait on partner
        this.show_left = false;
        this.session_copy = "Waiting for your partner to START";

        //update DB & check DB if both users pressed start
        this.start_bool = false;
        this.checkStartDB(true); //update DB ready = true

        //check every sec if both users pressed start
        this.startInterval = setInterval(() => this.checkStartDB(false,this.entry_order), 1000);
      }
    },

    checkStartDB(update_start,entry_order) {

      if (this.start_bool) { //both ready, terminate check
        clearInterval(this.startInterval);
        return;
      }

      //create get URL
      var request_url = '/api/checkstartdb?clientID=' + this.client_id;
      if (update_start) request_url += '&start=1';
      if (entry_order) request_url += '&order=' + entry_order;

      fetch(request_url)
      .then(response => {
        if (response.status !== 200) { //server error handling
          console.log(`Looks like there was a problem. Status code: ${response.status}`);
          return;
        }
        response.json().then(data => { //info about client added to active users in DB
          console.log("start data: ",data);
          
          if ('error' in data) { //error handling
            console.log(this.client_id,": checkStartDB error: ",data['error']);
            alert("checkStartDB error: " + data['error']);
            return;
          }

          if ('entry_order' in data) { //get entry order
            this.entry_order = parseInt(data['entry_order']);
            console.log("entry order:",this.entry_order);
          }

          if ('partner_start' in data) { //check if partner started
            let partner_start = parseInt(data['partner_start']);
            console.log("partner_start:",partner_start);
            if (partner_start > 0) { //both pressed start, begin meditation
              this.start_bool = true;
              this.beginMeditation();
            }
          }
        });
      })
      .catch(error => { //error handling
        console.log("Fetch error: " + error);
      });
    },

    beginMeditation() {

      this.show_left = true;
      this.left_copy = "";
      this.show_timer = true;
      this.session_copy = "Please begin meditation";

      console.log("med time is:",this.medTime);
      this.time_limit = (this.medTime > 0) ? this.medTime : 15 * 60;
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
      router.push({ name: 'SessionEnd' });
    },

    // onLoadTimerExpired() { //load timer triggers this which redirects to main expire function
      
    //   document.getElementById('load-wrapper').style.display = 'none';
    //   if (document.querySelector('iframe')) document.querySelector('iframe').style.visibility = "visible";
    //   this.session_copy = 'Say hello to each other';
    //   this.show_leave = true;
    //   this.show_timer = false;
    //   this.show_left = true;
    //   this.left_copy = "START";
    // },

    onTimerExpired() { //function runs based on stage of session when timer expires

      if (this.session_kick) { //kick user out 
        this.leaveSession();
      }
      else { //set debrief environment
        this.session_kick = true;
        this.time_limit = 5 * 60;
        this.show_timer = false;
        this.session_copy = "Thank your partner";
        this.bellRings(); //play ending bell
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

.load-wrapper {

  align-items: center;
  justify-content: center;
  display: flex;
  height: 358px;
  font-size: 36px;
}

</style>
