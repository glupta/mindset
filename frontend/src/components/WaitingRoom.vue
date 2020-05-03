<template>
  <div class="waiting-room">
    <SessionTopBar timerCopy='Session starts in ' v-on:timer-expired="onTimerExpired"></SessionTopBar>
    <div class='waiting-room-partner'>
        <p class='description'>
        You're here!
        <br>
        Waiting for your meditation buddy to join.
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
      msg: 'Welcome to Your Vue.js App'
    }
  },
  components: {
    SessionTopBar,
    SessionBottomBar
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
h1, h2 {
  font-weight: normal;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
