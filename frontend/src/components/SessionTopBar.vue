<template>
  <div class='session-top-bar'>
    <p class='session-time'>
      <br><Timer id='timer-clock' :timeLimit="timeLimit" @timer-expired="onTimerExpired"></Timer>
    </p>
    <p class='leave-button-div'>
    <br>
      <button id='leave-button-cont' class='leave-button' @click='leaveSession'>
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
        document.getElementById('timer-clock').style.visibility = "visible";
      }
      else {
        document.getElementById('timer-clock').style.visibility = "hidden";
      }
    },
    showLeave(newValue) {
      if (this.showLeave) {
        document.getElementById('leave-button-cont').style.display = "block";
      }
      else {
        document.getElementById('leave-button-cont').style.display = "none";
      }
    }
  },

  props: [
    'timeLimit',
    'showTimer',
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

.session-time {
  float: left;
  font-size: 16px;

}

.session-status-text {
  font-size: 16px;
}

.leave-button-div {
  float: right;
  width: 80px;
  height: 50px;
  /*position: relative;*/
  text-align: center;
}

.leave-button {
  background-color:#18a0fb;
	border-radius:6px;
	color:#ffffff;
  cursor:pointer;

  width: 80px;
  height: 20px;
  border: none;

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
