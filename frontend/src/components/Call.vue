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
//    testSession,
    roomURL: String
  },
  methods: {

    onTimerExpired() {
      if (this.debriefNext) {
        this.debriefNext = false;
        this.time_limit = 2 * 60;
        this.session_copy = "How was your session?";
      } else {

      	//remove user from active_users table
      	callFrame.leave();
      	callFrame.destroy();
        router.push({ name: "SessionEnd" });
      }
    }
  },
  mounted() {

    console.log("call is mounted, room url:",this.roomURL);
  	//take room ID from DB
    // let room_url = 'https://meditate-live.daily.co/';
    // room_url += (this.roomName == "") ? 'hello' : this.roomName;
    // console.log("room name",room_url);

    let dailycoScript = document.createElement('script');
    dailycoScript.addEventListener("load", function(event) {
      window.callFrame = window.DailyIframe.createFrame();
      callFrame.join({ url: this.roomURL});
      var elem = document.querySelector('iframe');
      elem.style.width= "375px";
      elem.style.height = "750px";
      elem.style.right= "0em";
      elem.style.bottom= "0em";
    });
    dailycoScript.setAttribute('src', 'https://unpkg.com/@daily-co/daily-js/dist/daily-iframe.js');
    document.head.appendChild(dailycoScript);

    this.debriefNext = true;
    this.time_limit = 1 * 60;
    this.session_copy = "Please begin meditation";
  },
  watch: {
    roomReady(newValue) {
      if (roomReady) {
        console.log("room is ready");
        //this.$refs.onRoomReady.JoinVideoCall(roomURL);
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
