<template>
<div class="home">
    <!--NavBar :useDotLogo="true"></NavBar-->
    <div class='onboarding-screen'>
        <div class='home-top-background-light'>
            <div class='home-background flexCC align-center justify-center'>
                <img class="logo" src="@/assets/Logo-V2-White.svg">
                <p class='description white-text'>
                    <br>
                    Science proves the many benefits of meditation.
                    <br>
                    Do you still struggle to practice it consistently?
                    <br>
                    Try meditating in fun random 1on1 video chats.
                    <br>
                    Sessions are for 15 min daily at 8 AM & 8 PM ET.
                    <br>
                    Let's help each other better our mental health!
                </p>
                <!--p class='white-text font-36'>
                    Next Session
                    <br>
                    <Timer class='timer-clock' :timeLimit='time_limit'></Timer>
                    <br><br>
                </p-->
                <div class='get-started-button align-center justify-center flexCR' @click='getStarted()'>
                    <p class='get-started-text'>
                        Get Started
                    </p>
                </div>
            </div>
        </div>
        <div class="main-body flexCC align-center justify-content">
            <p class='header'>
                How This Works
                <br><br>
            </p>
            <img class='circle-icon' src='@/assets/circle1.png'></img>
            <p class='header font-bold'>
                Get Ready
            </p>
            <p class='description content-width margin-bottom-32'>
                Go in the waiting room and test your settings.
            </p>    
            <img class='circle-icon' src='@/assets/circle2.png'></img>
            <p class='header font-bold'>
                Session Starts 
            </p>
            <p class='description content-width margin-bottom-32'>
                Enter video chat. Greet your assigned mate.
            </p>    
            <img class='circle-icon' src='@/assets/circle3.png'></img>
            <p class='header font-bold'>
                Practice Meditation
            </p>
            <p class='description content-width margin-bottom-32'>
                Start timer to meditate together until the bell.
            </p>    
            <img class='circle-icon' src='@/assets/circle4.png'></img>
            <p class='header font-bold'>
                Express Gratitude
            </p>
            <p class='description content-width margin-bottom-32'>
                Return to your senses. Thank your buddy.
            </p>
            <img class='circle-icon' src='@/assets/circle5.png'></img>
            <p class='header font-bold'>
                Leave Feedback
            </p>
            <p class='description content-width margin-bottom-32'>
                Exit session and review the experience.
            </p>

            <!--div class='get-started-button align-center justify-center flexCR margin-top-18 darker-blue'  @click='getStarted'>
                <p class='get-started-text'>
                    Get Started
                </p>
            </div-->
        </div>
        <div class='home-tips-background-light'>
            <div class='home-tips-background-dark white-text flexCC justify-center align-center'>
                <p class='header'>
                    Our Technique Advice
                </p>
                <p class='description content-width margin-bottom-32'>
                    Sit comfortably in a chair or on a cushion with your eyes closed. Straighten your back, and place your hands and feet in a relaxed position. 
                </p>
                <p class='description content-width margin-bottom-32'>
                    Imagine your thoughts are clouds. You want your mind to be a clear blue sky. Notice when thoughts appear and gently let them float away.
                </p>
                <p class='description content-width margin-bottom-32'>
                    If you find your mind racing, anchor one of your senses by counting your breaths, listening to ambient music, or lighting a scented candle.
                </p>
                <p class='description content-width margin-bottom-32'>
                    Try to minimize background sounds. In a noisy environment, mute your audio during the session and use headphones to block out distractions.
                </p>
                <p class='description content-width margin-bottom-32'>
                    Compatible with desktop, mobile, and tablet. For portable devices, turn on the 'Do Not Disturb' setting and consider using a stand.
                    <br><br><br>
                </p>
                <!--p class='description content-width padding-bottom-50'>
                    Optimize by meditating at the same time everyday, preferably in the morning or after a workout. Consider twice daily to experience greater effects.
                </p-->
            </div>
        </div>
    </div>
</div>
</template>

<script>
import NavBar from '@/components/NavBar';
import Timer from '@/components/Timer'
import router from '@/router';
export default {
  name: 'Home',
  data () {
    return {
      msg: 'Welcome to Your Vue.js App',
      time_limit: 0,
      time_sched: "N/A"
    }
  },
  components: {
    NavBar,
    Timer
  },
  methods: {
    getStarted() {
      router.push({ name: "ScheduleSession" });
      //router.push({ name: "WaitingRoom" });
    }
  },
  watch: {
    $route: {
      immediate: true,
      handler(to, from) {
        document.title = 'Home' || 'Some Default Title';
      }
    }
  },
  mounted() {

    document.body.style.backgroundColor = "#FFFFFF";

  //   fetch('/api/timedata')
  //   .then(response => {
  //     if (response.status !== 200) { //server error handling
  //       console.log(`Looks like there was a problem. Status code: ${response.status}`);
  //       return;
  //     }
  //     response.json().then(data => {

  //       console.log("time data:",data);
  //       if ('error' in data) { //error handling from testroom backend call
  //         console.log("request time error: ",data['error']);
  //         alert("request time error: " + data['error']);
  //         return;
  //       }

  //       let time_diff = parseInt(data['time_diff']); //change to 
  //       this.time_limit = time_diff;
  //     });
  //   })
  //   .catch(error => { //error handling
  //     console.log("Fetch error: " + error);
  //   });
  }
}

</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.darker-blue {
    background-color: #18A0FB !important;
}
.margin-top-18 {
    margin-top: 18px;
}
.home-background {
    background-color: #18A0FB;
    padding-top: 69px;
    padding-bottom: 65px;
    margin-bottom: 40px;
}
.home-background .description {
    font-size: 16px;
    margin-bottom: 48px;
    line-height: 1.5;
}

.home-top-background-light {
    padding-top: 20px;
    background-color: #2AD9FF;
}

.get-started-text {
    font-size: 24px;
}

.bold-text {
    font-weight: bold;
}

.font-36 {
  font-size: 24px;
}

.main-body .description {
    font-size: 16px;
}
.circle-icon {
    width: 38px;
    height: 38px;
    margin-bottom: 9px;
}
.header {
    font-size: 24px;
    line-height: 30px;
    margin-bottom: 6px;
}
.white-text {
    color: #FFFFFF;
}
.content-width {
    width: 315px;
}
.margin-bottom-32 {
    margin-bottom: 24px;
}
.get-started-button {
    background-color: #2AD9FF;
    border: 1px solid #2AD9FF;
    box-sizing: border-box;
    border-radius: 6px;
    width: 271px;
    height: 58px;
    color: #FFFFFF;
    font-size: 18px;
    line-height: 22px;
    cursor:pointer;
}
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

.logo {
  width: 198px;
  height: 30px;
  margin-bottom: 24px;
}
.home-tips-background-light {
    margin-top: 50px;
    padding-top: 20px;
    background-color: #2AD9FF;
}

.home-tips-background-dark {
    background-color: #18A0FB;
}

.home-tips-background-dark .header {
    padding-top: 50px;
}

.home-tips-background-dark .description {
    margin-top: 30px;
    font-size: 18px;
}
.padding-bottom-50 {
    padding-bottom: 50px;
}
</style>
