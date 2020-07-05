<template>
    <div class='session-end-screen'>
      <NavBar></NavBar>
        <br><br><br>
        <p class="header">
          Your session has ended.
          <br><br>
          Best of luck on your meditation journey!
        </p>
        <br><br>
        <!--p class='smalltext'>
            Did your buddy participate in the meditation practice?
        </p>
        <br>
        <div class='rating-section'>
          <br><br>
          <div style="position:relative; height:100%;">
            <div style="float: left; width: 15%;height: 40px;width: 40px;"></div>
            <div class='yes-button' v-bind:class="{ active: yesSelected}"  v-on:click='onSelectYes()'>
              <p style="margin-top:1.5em; color:#696969;">Yes</p>
            </div>
            <div style="float: left; width: 5%;height: 40px;width: 40px;"></div>
            <div class='no-button' v-bind:class="{ active: noSelected }"  v-on:click='onSelectNo()'>
              <p style="margin-top:1.5em; color:#696969;">No</p>
            </div>
          </div>
        </div>
        <br><br>
        <a class='schedule-appointment-button'  v-on:click='goToScheduleSession()'>New Session</a-->
    </div>
</template>

<script>
import NavBar from '@/components/NavBar'
import router from '../router'
export default {
  name: 'SessionEnd',
  data () {
    return {
      yesSelected: false,
      noSelected: false
    }
  },
  components: {
    NavBar
  },
  methods: {
    onSelectYes() {
      this.noSelected = false;
      this.yesSelected = true;
    },
    onSelectNo() {
      this.yesSelected = false;
      this.noSelected = true;
    },
    goToScheduleSession() {
      router.push({ name: "ScheduleSession" })
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
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.session-end-screen {
  font-family: 'DIN Condensed', sans-serif;
  font-size: 24px;
}

.smalltext {
  font-size: 14px;
}

.rating-section {
  width: 317px;
  height: 194px;
  left: 26px;
  top: 322px;
  background: rgba(196, 196, 196, 0.15);
  border-radius: 6px;
  margin: 0 auto;
  text-align: center;
}

.yes-button, .no-button{
  float: left;
  border: 2px solid #18A0FB;
  height: 100px;
  width: 100px;
  border-radius: 6px;
  background-color: #c7e9ff;
  color: #18A0FB;
}

.yes-button {
}

.no-button {
  
}

.schedule-appointment-button {
  font-size: 18px;
  font-family: 'DIN Condensed', sans-serif;
  border-radius: 5px;
  border: 2px solid #18A0FB;
  padding-top: 10px;
  padding-bottom: 10px;
  padding-right: 95px;
  padding-left: 95px;
  color: #18a0fb;
}

.active {
  background-color: #18A0FB;
}
</style>