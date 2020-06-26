<head>
  <title>Home</title>
</head>
<template>
  <div class="home">
    <NavBar :useDotLogo="true"></NavBar>
    <div class='onboarding-screen'>
    <div class='home-background flexCC align-center'>
        <img class="logo" src="@/assets/Logo-V2-White.svg">
        <p class='description white-text font-bold'>
            Unable to get yourself to meditate?
            <br>
            Meditate virtually with an accountability partner.
        </p>
        <div class='get-started-button align-center justify-center flexCR' v-on:click='getStarted()'>
            <p class='get-started-text'>
                Get Started
            </p>
        </div>
    </div>
    <div class="main-body flexCC align-center justify-content">
        <img class='circle-icon' src='@/assets/circle1.png'></img>
        <p class='header font-bold'>
            Decide when to meditate
        </p>
        <p class='description content-width margin-bottom-32'>
            Choose from 3 daily timings. Strive to keep a consistent practice, but sporatic sessions are always better than no sessions!
        </p>
        <img class='circle-icon' src='@/assets/circle2.png'></img>
        <p class='header font-bold'>
            Get ready, launch session
        </p>
        <p class='description content-width margin-bottom-32'>
            Before the session, join the waiting room and ensure your settings are good. Prepare your environment and your state of mind.
        </p>    
        <img class='circle-icon' src='@/assets/circle3.png'></img>
        <p class='header font-bold'>
            Meet partner, start meditation
        </p>
        <p class='description content-width margin-bottom-32'>
            When the session starts, you are randomly assigned a buddy. Greet and check in with each other. Decide whether to mute audio. Begin meditation!
        </p>    
        <img class='circle-icon' src='@/assets/circle4.png'></img>
        <p class='header font-bold'>
            Timer ends, debrief
        </p>
        <p class='description content-width margin-bottom-32'>
            Bells chime after a succesful session. Take your time returning to your senses. Describe the session experience to each other.
        </p>    
        <img class='circle-icon' src='@/assets/circle5.png'></img>
        <p class='header font-bold'>
            Finish up, schedule next
        </p>
        <p class='description content-width margin-bottom-32'>
            Exit session and give feedback. Let's schedule the next session to build from here!
        </p>
        <!--div class='get-started-button align-center justify-center flexCR margin-top-18 darker-blue'  v-on:click='getStarted()'>
            <p class='get-started-text'>
                Get Started
            </p>
        </div-->
    </div>
    <div class='home-tips-background-light'>
        <div class='home-tips-background-dark white-text flexCC justify-center align-center'>
            <p class='header'>
                Our Meditation Tips
            </p>
            <p class='description content-width margin-bottom-32'>
                Try to minimize background noise. If not possible, play ambient music through your headphones and mute the session.
            </p>
            <p class='description content-width margin-bottom-32'>
                Sit comfortably in a chair or on a cushion. Straighten your back, and place your hands and feet in a relaxed manner. 
            </p>
            <p class='description content-width margin-bottom-32'>
                Imagine your thoughts are clouds. You want your mind to be a clear blue sky. If clouds appear, observe them without judgement and let them float away.
            </p>
            <p class='description content-width margin-bottom-32'>
                Direct energy towards the center of your body. If you struggle to focus, consider anchoring one of your senses: count your breaths, listen to ambient music, or stare at a lit candle.
            </p>
            <p class='description content-width padding-bottom-50'>
                Optimize by meditating at the same time everyday, preferably in the morning or after a workout. Consider twice daily (morning and evening)7 to experience greater effects.
            </p>
        </div>
    </div>
</div>
  </div>
</template>

<script>
import NavBar from '@/components/NavBar';
import router from '../router';
export default {
  name: 'Home',
  data () {
    return {
      msg: 'Welcome to Your Vue.js App'
    }
  },
  components: {
    NavBar
  },
  methods: {
    getStarted() {
      //router.push({ name: "ScheduleSession" });
      router.push({ name: "WaitingRoom" });
    }
  },
  watch: {
    $route: {
      immediate: true,
      handler(to, from) {
        document.title = 'Home' || 'Some Default Title';
      }
    }
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
    font-size: 24px;
    line-height: 28px;
    margin-bottom: 48px;
}
.main-body .description {
    font-size: 14px;
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
    margin-bottom: 32px;
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
    font-size: 14px;
}
.padding-bottom-50 {
    padding-bottom: 50px;
}
</style>
