<template>
  <div class="waiting-room">
    <SessionTopBar :timeLimit=time_limit timerCopy='Session starts in ' v-on:timer-expired="onTimerExpired"></SessionTopBar>
    <div class='waiting-room-partner'>
        
        <p class='description' style='background-color:#2AD9FF;color:#FFFFFF;'>
        <br><br><br><br><br><br><br><br>
        You're here!
        <br>
        Waiting for your meditation<br>
        buddy to join.
        <br><br><br><br><br><br><br>
        <br><br><br><br><br><br><br>
        <br><br><br><br><br><br><br>
        <br><br><br><br><br><br><br>
        <br><br><br><br><br><br><br>
        <br><br><br><br><br><br><br>
        <br><br><br><br><br><br><br>
        </p>
        
    </div>
    <div class='video-chat-self'></div>
    <SessionBottomBar></SessionBottomBar>
  </div>
</template>

<script>
import SessionTopBar from '@/components/SessionTopBar'
import SessionBottomBar from '@/components/SessionBottomBar'
import router from '../router'
export default {
  name: 'WaitingRoom',
  data () {
    return {
      msg: 'Welcome to Your Vue.js App',
      time_limit: 0
    }
  },
  components: {
    SessionTopBar,
    SessionBottomBar
  },
  mounted() {
    this.time_limit = 30; //change this to time between current time and scheduled session time 
  },
  methods: {
    goToSession() {
      router.push({ name: "Call" })
    },
    onTimerExpired() {
      router.push({ name: "Call" })
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.waiting-room {
  font-family: 'DIN Condensed', sans-serif;
  font-size: 24px;
}
</style>
