<template>
    <div class='session-end-screen'>
      <NavBar></NavBar>
        <div>
          <p class="header">
            <br>
            Your session has ended.
            <br>
            Thank you for your participation.
            <br><br>
          </p>
        </div>
        <div>
          <!--p>
            Did your partner meditate in the session?
          </p-->
          <div class='rating-section'>
            <div style="position:relative; height:100%;">
              <p class='rating-section-text'>
                <br>
                Did your partner meditate in the session?
              </p>
              <div style="float: left; height: 16px; width: 40px;"></div>
              <div class="yes-button" :class="{active: yesSelected}" @click='onSelectYes'>
                <img :src='thumbsUp'/>
              </div>
              <div style="float: left; height: 16px; width: 40px;"></div>
              <div class='no-button' :class="{active: noSelected}" @click='onSelectNo'>
                <img :src="thumbsDown"/>
              </div>
              <div style="float: left; height: 16px; width: 40px;"></div>
            </div>
          </div>
        </div>
        <p>
          <br>
          What did you notice about your thoughts?
          <br>
          Keep a log of your observations in a journal.
          <br><br>
          We hope you enjoy the benefits of meditation!
          <br>
          Email your feedback to <a href="mailto:meditateliveorg@gmail.com">hello@meditatelive.org</a>
          <br><br>
        <button class='homepage-button'  @click='goToHomepage'>Back to Home</button>
    </div>
</template>

<script>
import NavBar from '@/components/NavBar'
import router from '@/router'
export default {
  name: 'SessionEnd',
  data () {
    return {
      yesSelected: false,
      noSelected: false,
      thumbsUp: require('@/assets/thumbsupblue.png'),
      thumbsDown: require('@/assets/thumbsdownblue.png')
    }
  },
  components: {
    NavBar
  },
  methods: {
    onSelectYes() {
      this.noSelected = false;
      this.thumbsDown = require('@/assets/thumbsdownblue.png');

      this.yesSelected = true;
      this.thumbsUp = require('@/assets/thumbsupwhite.png');
    },
    onSelectNo() {
      this.yesSelected = false;
      this.thumbsUp = require('@/assets/thumbsupblue.png');

      this.noSelected = true;
      this.thumbsDown = require('@/assets/thumbsdownwhite.png');
    },
    goToScheduleSession() {
      router.push({ name: "ScheduleSession" });
    },
    goToHomepage() {
      router.push({ name: "Home" });
    }
  },

  watch: { //set page title
    $route: {
      immediate: true,
      handler(to, from) {
        document.title = 'Session Ended' || 'Some Default Title';
      }
    }
  },

  mounted() {
    document.body.style.backgroundColor = "#18A0FB";
  },

  beforeDestroyed() {
    document.body.style.backgroundColor = "#FFFFFF";
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.session-end-screen {
  /*font-family: 'DIN Condensed', sans-serif;*/
  font-size: 18px;
  line-height: 1.5;
  background-color: #18A0FB;
  color: #FFFFFF;
  position: absolute;
  top: 0;
  bottom: 0;
  left: 0;
  right: 0;
}

.session-end-top {
  background-color: #18A0FB;
  color: #FFFFFF;
}

.session-end-bottom {
  background-color: #FFFFFF;
  color: #696969;
}

.smalltext {
  font-size: 14px;
}

.rating-section {
  width: 328px;
  height: 194px;
  left: 26px;
  top: 322px;
  background-color: #FFFFFF;
  /*background: rgba(196, 196, 196, 0.15);*/
  border-radius: 6px;
  margin: 0 auto;
  text-align: center;

  display: flex;               /* establish flex container */
  align-items: center;
}

.rating-section-text {
  color: #18A0FB;
  font-size: 16px;
}

.yes-button, .no-button{
  float: left;
  border: 2px solid #18A0FB;
  height: 100px;
  width: 100px;
  border-radius: 6px;
  background-color: #c7e9ff;
  color: #18A0FB;

  position:relative;
  top: 21px;
  text-align: center;
  vertical-align: middle;

  display: flex;
  justify-content: center;
}

.yes-button {
}

.no-button {
  
}

.yes-button img {
  display: block;
  margin: auto;
}

.no-button img {
  display: block;
  margin: auto;
}

.schedule-appointment-button {
  font-size: 18px;
  /*font-family: 'DIN Condensed', sans-serif;*/
  border-radius: 5px;
  border: 2px solid #18A0FB;
  padding-top: 10px;
  padding-bottom: 10px;
  padding-right: 95px;
  padding-left: 95px;
  color: #18a0fb;
}

.homepage-button {
  font-size: 18px;
  border-radius: 6px;
  border: 1px solid #2AD9FF;
  color: #FFFFFF;
  background-color: #2AD9FF;

  box-sizing: border-box;
  line-height: 22px;
  width: 271px;
  height: 58px;

  cursor:pointer;
}

.active {
  background-color: #18A0FB;
}
</style>