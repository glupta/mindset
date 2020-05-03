<template>
  <div class="schedule-confirmation">
    <NavBar></NavBar>
    <br><br><br><br>
    <p class='mydescription'>
        It's set! You will receive an email 30 minutes before your session.
    </p>
    <br>
    <a class='scheduled-time' >May 3 at 1:00pm PST</a>
    <br><br><br><br><br>
    <p class='mydescription'>
        Want to do a test run?
    </p>
    <br>
    <a class='test-session-button' v-on:click="testSession()">Test Session</a>
  </div>
</template>

<script>
import NavBar from '@/components/NavBar';
import router from '../router';
export default {
  name: 'ScheduleConfirmation',
  data () {
    return {
      msg: 'Welcome to Your Vue.js App'
    }
  },
  components: {
    NavBar
  },
  methods: {
    testSession() {
      router.push({
        name: "Call",
        props: {
          testSession: true
        }
      })
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.schedule-confirmation {
  font-family: 'DIN Condensed', sans-serif;
  font-size: 24px;
}

.mydescription{
  padding-left: 10px;
  padding-right: 10px;
  text-align: center;
}

.scheduled-time {
	background-color:rgba(236, 236, 236, 0.38);
	border-radius:5px;
	display:inline-block;
	cursor:pointer;
	color: #18a0fb;
  font-weight: 750;
	font-family: 'DIN Condensed', sans-serif;
	font-size:22px;
	padding:30px 50px;
	text-decoration:none;
}

.test-session-button {
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
</style>
