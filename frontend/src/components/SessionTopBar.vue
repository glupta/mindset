<template>
  <div class='session-top-bar'>
    <!--p class='session-time'>
      <br><
    </p-->
    <p class='bell-button-wrapper'>
      <Timer id='timer-clock' :timeLimit="timeLimit" @timer-expired="onTimerExpired"></Timer>
      <button id='bell-button' class='bell-button' @click='bellRings'>
        Bell
      </button>
    </p>
    <p class='leave-button-wrapper'>
    <br>
      <button id='leave-button' class='leave-button' @click='leaveSession'>
        Leave
      </button>
    </p>
    <!--div class='session-status'-->
      <p class='session-status-text'>
        <br>{{sessionCopy}}
      </p>
    <!--/div-->
  </div>
</template>

<script>
import Timer from '@/components/Timer'
export default {
  name: 'SessionTopBar',
  data () {
    return {
      msg: 'Welcome to Your Vue.js App',
      sessionCopy: '',
    }
  },
  components: {
    Timer
  },
  methods: {

    bellRings() {
      this.$emit('bell-rings')
    },

    leaveSession() {
      this.$emit('leave-session')
    },

    onTimerExpired() {
      this.$emit('timer-expired');
    }
  },

  watch: {
    showTimer(newValue) {
      if (this.showTimer) {
        document.getElementById('timer-clock').style.display = "block";
      }
      else {
        document.getElementById('timer-clock').style.display = "none";
      }
    },
    showBell(newValue) {
      if (this.showBell) {
        document.getElementById('bell-button').style.display = "block";
      }
      else {
        document.getElementById('bell-button').style.display = "none";
      }
    },
    showLeave(newValue) {
      if (this.showLeave) {
        document.getElementById('leave-button').style.display = "block";
      }
      else {
        document.getElementById('leave-button').style.display = "none";
      }
    }
  },

  props: [
    'timeLimit',
    'showTimer',
    'showBell',
    'showLeave',
    'sessionCopy'
  ]
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.session-top-bar {
  height: 50px;
}

.bell-button-wrapper {
  float: left;
  width: 100px;
  height: 50px;
  text-align: center;
  align-items: center;
  justify-content: center;
  margin: 0 auto;
  display: flex;
}

.bell-button {
  background-color:#18a0fb;
  border-radius:6px;
  color:#ffffff;
  cursor:pointer;

  width: 80px;
  height: 20px;
  border: none;
  box-sizing: border-box;
}

.session-time {
  float: left;
  font-size: 16px;
}

.session-status-text {
  font-size: 16px;
}

.leave-button-wrapper {
  float: right;
  width: 100px;
  height: 50px;
  /*position: relative;*/
  text-align: center;
  align-items: center;
  justify-content: center;
  margin: 0 auto;
  display: flex;
}

.leave-button {
  background-color:#18a0fb;
	border-radius:6px;
	color:#ffffff;
  cursor:pointer;

  width: 80px;
  height: 20px;
  border: none;
  box-sizing: border-box;

/*
  font-family: 'DIN Condensed', sans-serif;
  padding-top: 8px;
  padding-bottom: 8px;
  padding-right: 32px;
  padding-left: 32px;

  display:inline-block;
  position: absolute;
  top: 50%;
  left: 50%;
  
*/
}

</style>
