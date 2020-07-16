<template>
  <div class='session-top-bar'>
    <!--p class='session-time'>
      <br><
    </p-->
    <div class='left-wrapper' id='left-wrapper'>
      <Timer id='timer-clock' :timeLimit="timeLimit" @timer-expired="onTimerExpired"></Timer>
      <button id='left-button' class='left-button' @click='leftAction'>
        {{leftCopy}}
      </button>
    </div>
    <p class='leave-button-wrapper'>
    <br>
      <button id='leave-button' class='leave-button' @click='leaveSession'>
        LEAVE
      </button>
    </p>
    <div class='session-status'>
      <p class='session-status-text'>
        {{sessionCopy}}
      </p>
    </div>
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

    leftAction() {
      this.$emit('left-action')
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
        if (this.leftCopy == '') {
          document.getElementById('left-wrapper').style.display = "none";
        }
      }
    },
    leftCopy(newValue) {
      if (this.leftCopy !== '') {
        document.getElementById('left-wrapper').style.display = "flex";
        document.getElementById('left-button').style.display = "block";
      }
      else {
        document.getElementById('left-button').style.display = "none";
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
    'leftCopy',
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

.left-wrapper {
  float: left;
  width: 100px;
  height: 50px;
  text-align: center;
  align-items: center;
  justify-content: center;
  margin: 0 auto;
  display: flex;
}

.left-button {
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

.session-status {
  height: 50px;
  text-align: center;
  align-items: center;
  justify-content: center;
  margin: 0 auto;
  display: flex;
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
