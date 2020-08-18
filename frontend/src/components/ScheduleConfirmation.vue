<template>
  <div class="schedule-confirmation">
    <NavBar></NavBar>
    <br><br><br><br>
    <p class='mydescription'>
      {{sched_copy}}
    </p>
    <br>
    <!--a class='scheduled-time'>{{sched_time}}</a>
    <br><br><br><br><br>
    <p class='mydescription'>
        Want to do a test run?
    </p>
    <br>
    <a class='test-session-button' @click="testSession()">Test Session</a-->
    <button class='plan-button' @click='planSession()'>Back to Schedule</button>
  </div>
</template>

<script>
import NavBar from '@/components/NavBar';
import router from '../router';
export default {
  name: 'ScheduleConfirmation',
  data () {
    return {
      msg: 'Welcome to Your Vue.js App',
      sched_copy: 'Thank you for confirming your session.',
      sched_time: ''
    }
  },
  components: {
    NavBar
  },

  mounted() {

    document.body.style.backgroundColor = "#2AD9FF";
    this.session_hash = this.$route.query.id;
    
    if (!this.session_hash) { //if id query not given
      this.sched_copy = 'Your session was not confirmed.';
      return;
    }

    //check first letter (u = user and p = partner)
    if (this.session_hash.charAt(0) == 'u') {
      this.user_bool = true;
    }
    else if (this.session_hash.charAt(0) == 'p') {
      this.user_bool = false;
    }

    //call server with session type and hash
    let fetch_url = '/api/schedemail?id=' + this.session_hash;
    fetch(fetch_url)
    .then(response => {
      if (response.status !== 200) { //server error handling
        console.log(`Looks like there was a problem. Status code: ${response.status}`);
        return;
      }
      response.json().then(data => {

        //console.log("wr time data:",data);
        if ('error' in data) { //error handling from testroom backend call
          //console.log(this.client_id,": flush active users DB error: ",data['error']);
          alert("sched confirm error: " + data['error']);
          return;
        }

        if ('success' in data) {
          console.log("successful");
        }
      });
    })
    .catch(error => { //error handling
      console.log("Fetch error: " + error);
    });

    //search database for hash
    //if not found, kick out to error alert
    //if partner, update partner id and confirm time
    //if user, update confirm time and get all details
    //send confirmation email with link to waiting room
    //if type=claim, notify user of partner confirmation
    //set up reminder with link for waiting room 5 min before session
    //set up text reminder
    //waiting room link is hash and type
    //click to join waiting room
    //if more than 5 minutes, countdown clock
    //Enter room within 5 minute window + 1 min buffer
    //check if room name = hash exists
    //if not, create room = hash
    //join hash room
    //kick out at 5 min after sched time
    //press start
    //if user, update user_start when starts['n ']
    //if partner, update partner_start when starts
    //start meditation together
    //if reload and start field is empty (before start)
    //if reload and start field is filled and other is empty (waiting)
    //if reload and start field is filled and other is filled within 15 min of later (during)
    //if reload and start field is filled and other is filled after 15 min of later (debrief)
    //kick out at sched + duration + 10 min


  },

  methods: {
    testSession() {
      router.push({
        name: "Call",
        props: {
          testSession: true
        }
      })
    },

    planSession() {
      router.push({ name: "ScheduleSession" });
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

.plan-button {
  font-size: 18px;
  border-radius: 6px;
  border: 1px solid #18A0FB;
  
  color: #FFFFFF;
  background-color: #18A0FB;

  box-sizing: border-box;
  line-height: 22px;
  width: 271px;
  height: 58px;

  cursor: pointer;
  position: relative;
}
</style>
