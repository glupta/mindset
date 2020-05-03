<template>
    <div class="schedule-session">
        <NavBar></NavBar>
        <br>
        <p class="header">Pick a time that works for you</p>
        <br>
        <input type="email" id ="email_input" placeholder='  Email' />
        <br><br>
        <select class="myselection" id="date_selection" name="dates">
          <option value="" disabled selected>Day</option>
          <option value="monday">Mon May 3, 2020</option>
          <option value="tuesday">Tues May 4, 2020</option>
          <option value="wednesday">Wed May 5, 2020</option>
          <option value="thursday">Thurs May 6, 2020</option>
        </select>
        <br><br>
        <select class="myselection" id="time_selection" name="times" disabled>
          <option value="" disabled selected>Time</option>
          <option value="monday">11 a.m. PST</option>
          <option value="tuesday">1 p.m. PST</option>
          <option value="wednesday">4 p.m. PST</option>
          <option value="thursday">7 p.m. PST</option>
        </select>
        <br><br>
        <a class='submit-button' v-on:click="submit()">Submit</a>
    </div>
</template>

<script>
import NavBar from '@/components/NavBar';
import router from '../router';
export default {
  name: 'ScheduleSession',
  mounted(){
    //enable the second dropdown only once the first one has been completed
    document.getElementById("date_selection").onchange = function () {
      if (this.value != "") {
        document.getElementById("time_selection").disabled = false;
      }
    }
  },
  components: {
    NavBar
  },
  methods: {
    submit() {
      router.push({ name: "ScheduleConfirmation" });
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.schedule-session {
  font-size: 24px;
}

#email_input {
  font-size: 24px;
  font-family: 'DIN Condensed', sans-serif;
  width: 280px;
  height: 30px;
  border-radius: 25px;
  border: 2px solid #18A0FB;
  padding: 20px;
  color: #18a0fb;
  background-color: rgba(236, 236, 236, 0.38);
}

::placeholder { /* Chrome, Firefox, Opera, Safari 10.1+ */
  color: #18a0fb;
  opacity: 1; /* Firefox */
}

.myselection {
  font-size: 24px;
  font-family: 'DIN Condensed', sans-serif;
  width: 320px;
  border-radius: 25px;
  border: 2px solid #18A0FB;
  padding: 20px;
  color: #18a0fb;
  background-color: rgba(236, 236, 236, 0.38);
}

.submit-button {
	background-color:#18a0fb;
	border-radius:25px;
	display:inline-block;
	cursor:pointer;
	color:#ffffff;
	font-family: 'DIN Condensed', sans-serif;
	font-size:22px;
	padding:30px 140px;
	text-decoration:none;
}

.appointment-form {
  color: #18A0FB;
}
</style>
