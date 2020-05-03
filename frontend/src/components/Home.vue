<template>
  <div class="home">
    <NavBar></NavBar>
    <div class='onboarding-screen'>
    <div class='home-background'>
        <div class='icon-logo'></div>
        <p class='description'>
            Unable to get yourself to meditate?
            <br>
            Meditate virtually with an accountability partner.
        </p>
        <div class='get-started-button'>
            <p class='get-started-text'>
                Get Started
            </p>
        </div>
    </div>
    <div class='step-icon-circle'>
        <div class='step-icon-one'></div>
    </div>
    <p class='header'>
        Decide when to meditate
    </p>
    <p class='description'>
        Choose from 3 daily timings. Strive to keep a consistent practice, but sporatic sessions are always better than no sessions!
    </p>
    <div class='step-icon-circle'>
        <div class='step-icon-two'></div>
    </div>
    <p class='header'>
        Get ready, launch session
    </p>
    <p class='description'>
        Before the session, join the waiting room and ensure your settings are good. Prepare your environment and your state of mind.
    </p>    
    <div class='step-icon-circle'>
        <div class='step-icon-three'></div>
    </div>
    <p class='header'>
        Meet partner, start meditation
    </p>
    <p class='description'>
        When the session starts, you are randomly assigned a buddy. Greet and check in with each other. Decide whether to mute audio. Begin meditation!
    </p>    
    <div class='step-icon-circle'>
        <div class='step-icon-four'></div>
    </div>
    <p class='header'>
        Timer ends, debrief
    </p>
    <p class='description'>
        Bells chime after a succesful session. Take your time returning to your senses. Describe the session experience to each other.
    </p>    
    <div class='step-icon-circle'>
        <div class='step-icon-five'></div>
    </div>
    <p class='header'>
        Finish up, schedule next
    </p>
    <p class='description'>
        Exit session and give feedback. Let's schedule the next session to build from here!
    </p>    
    <div class='get-started-button'>
        <p class='get-started-text'>
            Get Started
        </p>
    </div>
    <div class='home-tips-background-light'>
        <div class='home-tips-background-dark'>
            <p class='header'>
                Our Meditation Tips
            </p>
            <p class='description'>
                Try to minimize background noise. If not possible, play ambient music through your headphones and mute the session.
            </p>
            <p class='description'>
                Sit comfortably in a chair or on a cushion. Straighten your back, and place your hands and feet in a relaxed manner. 
            </p>
            <p class='description'>
                Imagine your thoughts are clouds. You want your mind to be a clear blue sky. If clouds appear, observe them without judgement and let them float away.
            </p>
            <p class='description'>
                Direct energy towards the center of your body. If you struggle to focus, consider anchoring one of your senses: count your breaths, listen to ambient music, or stare at a lit candle.
            </p>
            <p class='description'>
                Optimize by meditating at the same time everyday, preferably in the morning or after a workout. Consider twice daily (morning and evening) to experience greater effects.
            </p>
        </div>
    </div>
</div>
  </div>
</template>

<script>
import NavBar from '@/components/NavBar';
export default {
  name: 'Home',
  data () {
    return {
      msg: 'Welcome to Your Vue.js App'
    }
  },
  components: {
    NavBar
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
