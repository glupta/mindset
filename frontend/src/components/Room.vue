
<template>
  <!--div class='call'>
    <SessionTopBar :showTimer=show_timer :showLeft=show_left :leftCopy=left_copy :showLeave=show_leave :timeLimit=time_limit :sessionCopy=session_copy @timer-expired="onTimerExpired" @left-action="startTimer" @leave-session="leaveSession"></SessionTopBar>
  </div-->

  <div class="fullpages-room-pre-permissions">
    <WebNavbarRoom @start-timer="startTimer" :timeLimit="time_limit" :sessionCopy="session_copy" :sessionCopyRight="session_copy_right" @timer-expired="endTimer" class="web-navbar-room-pre"></WebNavbarRoom>
    <!--div class="relative-wrapper1">
      <div class="partner"></div>
      <div class="user"></div-->
      <!--RoomCamera class="room-camera"></RoomCamera
      ><RoomMic class="room-mic"></RoomMic
      ><RoomMore class="room-more"></RoomMore
      ><RoomNetwork class="room-network"></RoomNetwork-->
    </div>
  </div>

</template>

<script>
import WebNavbarRoom from '@/components/WebNavbarRoom'
import router from '@/router'
export default {
  name: "Call",
  data () {
    return {
      time_limit: 0,
      session_copy: '',
      session_copy_right: '',
      session_status: ''
      DAILYID: 'meditate-live' //use meditate or meditate-live
    }
  },
  components: {
    WebNavbarRoom
  },
  props: {
    clientID: String,
    roomName: String,
    medTime: Number,
    skipStart: Number,
    sessionType: String
  },

  mounted() {

    this.killVidChat(); //delete any loose iframe
    this.session_status = 'start';
    this.room_name = "room1";

    if (this.roomName) {
      this.room_name = this.roomName;
    }

    this.sessionLoad();

    // if (this.clientID && this.roomName) { //connect if client ID & room name given

    //   this.client_id = this.clientID;
    //   this.room_name = this.roomName;
  //     this.show_timer = false;
  //     this.session_copy = 'Say hello to each other';
  //     this.time_limit = 5 * 60;
  //     this.session_kick = true;

  //     // if (this.calBool > 0) {
  //     //   //run function to create room if does not exist with hash
  //     // }
  //     // else {
  //       this.sessionLoad();
  //     //}
  //     //set cookie session status as load
  //   }
  //   else if (this.$cookies.isKey('medlive')) { //use cookie to find room

  //     let cookie_obj = this.$cookies.get('medlive');
  //     this.client_id = cookie_obj.client_id;
  //     console.log(this.client_id,": found cookie");

  //     //if start_time exists
  //     //  let time_left = 15 - (current_time - start_time)
  //     //  beginMeditation(time_left)
  //     if (cookie_obj.start_time) {
  //       fetch('/api/timedata')
  //       .then(response => {
  //         if (response.status !== 200) { //server error handling
  //           console.log(`Looks like there was a problem. Status code: ${response.status}`);
  //           return;
  //         }
  //         response.json().then(data => {

  //           console.log("call time data:",data);
  //           if ('error' in data) { //error handling from testroom backend call
  //             console.log(this.client_id,": meditation time error: ",data['error']);
  //             alert("meditation time error: " + data['error']);
  //             return;
  //           }

  //           //set cookie session status as meditation

  //           let time_current = new Date(data['time_current']);
  //           let time_start = new Date(cookie_obj.start_time);
  //           let time_diff = 15 * 60 - parseInt((time_current - time_start) / 1000);
  //           console.log('start:',time_start,'current:',time_current,'diff:',time_diff);

  //           if (time_diff > 0) {
  //             this.checkRoom(); //get room data and load session
  //             this.beginMeditation(time_diff); //set environment for meditation
  //           }
  //           else {
  //             this.connectionLost();
  //           }
  //         });
  //       })
  //       .catch(error => { //error handling
  //         console.log("Fetch error: " + error);
  //       });
  //     }
  //     else {
  //       this.connectionLost();
  //     }
  //   }
  //   else { //kick user out if no cookie
  //     console.log("no cookie, kick out");
  //     router.push({ name: "SessionEnd" });
  //     return;
    // }
  },

  watch: { //set page title
    $route: {
      immediate: true,
      handler(to, from) {
        document.title = 'Meditation Room' || 'Some Default Title';
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

    //remove cookie session status
  },

  Destroyed() {
    //delete vid chat
    this.killVidChat();
  },

  methods: {

    sessionLoad() { //load video chat with room name

      var entry = {
        room_name: this.room_name
      };

      fetch('/api/roomtoken', { //get room token
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
            console.log(":roomtoken error: ",data['error']);
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
              elem.style.top = "72px";
              elem.style.right = "0";
              elem.style.width = "100%";
              elem.style.height = "calc(100% - 72px)";
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

      //load audio file, overcome autoplay issue
      if (!this.med_bell) {
        this.med_bell = new Audio(require('@/assets/meditationbell.mp3'));
        //console.log('new audio');
      }

      //workaround to loop audio on mute
      this.med_bell.muted = true;
      this.med_bell.loop = true;
      this.med_bell.play();

      this.session_copy = "Waiting for your partner to START";

      //check if both users pressed start
      this.checkStartCal(true);
      this.startInterval = setInterval(() => this.checkStartCal(false), 1000);
    },

    checkStartCal(update_start) { //check every sec if both users pressed start

      if (this.start_bool) { //both ready, terminate check
        clearInterval(this.startInterval);
        return;
      }

      //create get URL
      var request_url = '/api/checkstartcal?id=' + this.sessionType + this.room_name;
      if (update_start) request_url += '&start=1';

      fetch(request_url)
      .then(response => {
        if (response.status !== 200) { //server error handling
          console.log(`Looks like there was a problem. Status code: ${response.status}`);
          return;
        }
        response.json().then(data => { //info about client added to active users in DB
          console.log("start data: ",data);
          
          if ('error' in data) { //error handling
            console.log(this.client_id,": checkStartCal error: ",data['error']);
            alert("checkStartCal error: " + data['error']);
            return;
          }

          if ('ready' in data) {
            console.log("not ready");
          }
          else {
          //if ('user_start' in data && 'partner_start' in data) { //check if both started
            let user_start = data['user_start'];
            let partner_start = data['partner_start'];
            console.log("user:",user_start,"partner:",partner_start);
            //if (user_start != '' && parter_start != '') { //both pressed start, begin meditation
              this.start_bool = true;
              this.beginMeditation();
            //}
          }
        });
      })
      .catch(error => { //error handling
        console.log("Fetch error: " + error);
      });
    },

    beginMeditation() { //begin meditation for duration

      this.session_status = 'meditate';
      this.session_copy = "Please begin meditation";
      this.session_copy_right = 'Session started';

      console.log("med time is:",this.medTime);
      this.time_limit = (this.medTime > 0) ? this.medTime : 15 * 60;

      //set cookie for start time
      // if (this.$cookies.isKey('medlive')) {
      //   fetch('/api/timedata')
      //   .then(response => {
      //     if (response.status !== 200) { //server error handling
      //       console.log(`Looks like there was a problem. Status code: ${response.status}`);
      //       return;
      //     }
      //     response.json().then(data => {

      //       console.log("call time data:",data);
      //       if ('error' in data) { //error handling from testroom backend call
      //         console.log(this.client_id,": meditation time error: ",data['error']);
      //         alert("meditation time error: " + data['error']);
      //         return;
      //       }
      //       //set cookie session status as meditation

      //       let cookie_obj = this.$cookies.get('medlive');
      //       cookie_obj.start_time = data['time_current'];
      //       let cookie_json = JSON.stringify(cookie_obj);
      //       this.$cookies.set('medlive',cookie_json,-1);
      //       console.log("medlivetime:",this.$cookies.get('medlive'));
      //     });
      //   })
      //   .catch(error => { //error handling
      //     console.log("Fetch error: " + error);
      //   });
      // }
    },

    endTimer() {

      if (this.session_status == 'meditate') {
        this.bellRings();
        this.time_limit = 300;
        this.session_copy = "Thank your partner";
        this.session_copy_right = "Session ended";
        this.session_status = 'done';
      }
      else if (this.session_status == 'done') {
        router.push({ name: 'SessionEnd2' });
      }
      else {
        router.push({ name: 'FullscreenTest' });
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

      this.med_bell.play();

      //set cookie session status as debrief
    },

    connectionLost() { //sets environment if connection lost
      //reset session environment 
      this.show_left = false;
      this.session_copy = 'Connection lost, timer stopped.';
      this.time_limit = 20 * 60; 
      this.checkRoom(); //get room data and load session
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
.fullpages-room-pre-permissions {
  padding: 0px 0px 73px;
  display: flex;
  flex-direction: column;
  align-items: center;
}
.web-navbar-room-pre {
  margin-bottom: 16px;
}
.relative-wrapper1 {
  display: flex;
  align-items: flex-start;
  position: relative;
}
.partner {
  width: 1402px;
  height: 863px;
  background-color: rgba(250, 251, 251, 1);
  margin-left: 1px;
  position: relative;
  border: 1px solid rgba(216, 228, 228, 1);
}
.user {
  width: 304px;
  height: 192px;
  background-color: rgba(171, 174, 168, 1);
  position: absolute;
  right: 548px;
  bottom: 24px;
}
.room-camera {
  position: absolute;
  left: 40px;
  bottom: 24px;
}
.room-mic {
  position: absolute;
  left: 136px;
  bottom: 24px;
}
.room-more {
  position: absolute;
  right: 134px;
  bottom: 24px;
}
.room-network {
  position: absolute;
  right: 38px;
  bottom: 24px;
}
</style>
