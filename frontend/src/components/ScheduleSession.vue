<template>
  <div class="schedule-session">
    <NavBar></NavBar>
    <p class='description'>
      <br><br>
      Public Sessions:
      <br>
      <div class="session-table">
        <div class="session-headers">
          <div v-for="sesh of session_col" class="session-cells">{{sesh}}</div>
        </div>
        <div v-for="(sesh,i) of sessions" class="session-rows" :key="'session-'+i" ref="session_rows" @click="onClaim(i)">
          <div class="session-cells">
            <input type="radio" name="session-radio">
          </div>
          <div v-for="cell of sesh" class="session-cells">
            {{cell}}
          </div>
        </div>
      </div>
      <br>
      <hr>
      <br>
      New Session:
      <br>
      <select v-model="day_selected" @change="updateDaySched()">
        <option disabled value="">date</option>
        <option v-for='(day,k) in week':key="'day-'+k" ref="day_rows">{{day}}</option>
      </select>
      &nbsp;
      <select v-model="hour_selected">
        <option disabled value="">hr</option>
        <option v-for='hour in hours'>{{hour}}</option>
      </select>
      :
      <select v-model="min_selected">
        <option disabled value="">min</option>
        <option>00</option>
        <option>30</option>
      </select>
      <input type="radio" id="AM" value="AM" v-model="ap_selected">
      <label for="AM">AM</label>
      <input type="radio" id="PM" value="PM" v-model="ap_selected">
      <label for="PM">PM</label>
      <br><br>
      Duration (min):
      <input v-model='user_duration' style="width: 3ch;">
      &nbsp;&nbsp;&nbsp;Private:
      <input type="checkbox" id="priv_check" v-model="priv_selected">
      <br><br>
      Invite friends:
      <textarea v-model='invite_email' placeholder='emails separated by comma'></textarea>
      <br><br>
      <hr>
      <br>
      Confirm Time: {{sched_time_format}}
      <br><br>
      Your email:
      <input v-model='user_email'>
      <br><br>
      <button class='test-session-button' @click="onSubmit">Submit</button>
      <br><br>
      {{submit_copy}}
    </p>
  </div>
</template>

<script>
import Timer from '@/components/Timer'
import NavBar from '@/components/NavBar'
import router from '../router'
export default {
  name: 'ScheduleSession',
  data () {
    return {
      msg: 'Welcome to Your Vue.js App',
      time_limit: 0,
      day_selected: '',
      week: [],
      week_dates: [],
      hour_selected: '',
      hours: [],
      min_selected: '',
      ap_selected: 'AM',
      user_duration: '15',
      priv_selected: '',
      user_email: '',
      invite_email: '',
      sessions: [],
      session_col: ['Select','User','Time','Duration'],
      sched_time: '',
      sched_time_format: 'not selected',
      session_type: '',
      session_dates: [],
      session_hashes: [],
      session_hash: '',
      session_type: '',
      session_id: 0,
      submit_copy: ''
    }
  },
  components: {
    Timer,
    NavBar
  },
  
  mounted() {

    document.body.style.backgroundColor = "#2AD9FF";

    //get user_id
    if (this.$cookies.isKey('medlive')) {
      let cookie_obj = this.$cookies.get('medlive');
      this.user_id = cookie_obj.client_id;
      console.log(this.user_id,": found cookie");
    }
    else {
      this.user_id = Math.random().toString(36).slice(-5);
      let cookie_obj = new Object();
      cookie_obj.client_id = this.user_id;
      let cookie_json = JSON.stringify(cookie_obj);
      this.$cookies.set('medlive',cookie_json,-1);
      console.log("create cookie");
    }

    this.refreshSessions(); //get session list

    fetch('/api/timedata') //get current datetime
    .then(response => {
      if (response.status !== 200) { //server error handling
        console.log(`Looks like there was a problem. Status code: ${response.status}`);
        return;
      }
      response.json().then(data => {

        console.log("time data:",data);
        if ('error' in data) { //error handling from testroom backend call
          console.log(this.client_id,": request time error: ",data['error']);
          alert("request time error: " + data['error']);
          return;
        }

        // this.time_currentUTC = new Date(data['time_current']);
        // this.offset = new Date().getTimezoneOffset();
        // this.time_current = moment(this.time_currentUTC).subtract(this.offset, 'm').toDate();
        // console.log('current:',this.time_current,'currentUTC:',this.time_currentUTC,'offset:',this.offset);
        
        var moment = require('moment');
        moment().format();

        //get today's date
        this.time_current = new Date(data['time_current']);
        let today = new Date(this.time_current.getFullYear(),this.time_current.getMonth(),this.time_current.getDate());

        for (let i = 0; i < 7; i++) { //find next 6 days in weeks

          let today_format = today;
          let today_str = today.toString();
          this.week_dates.push(today_str);
          this.week.push(moment(today_format).format('ddd, MMM Do'));
          console.log("today:",today,"format:",today_format);
          today.setDate(today.getDate() + 1);
        }

        console.log("current:",this.time_current,"today:",today);
        console.log("week:",this.week,"weekdates:",this.week_dates);

        for (let i = 1; i <= 12; i++) { //create list of 24 hours
          this.hours.push(i)
        }
      });
    })
    .catch(error => { //error handling
      console.log("Fetch error: " + error);
    });
  },

  watch: {
    
    day_selected(newValue) { //when user selects day
      var moment = require('moment');
      moment().format();
      let i = this.week.indexOf(this.day_selected);
      if (i < 0) {
        console.log('did not find');
      }
      else {
        let h = 0;
        let m = 0;
        if (this.sched_time != '' && this.session_type == 'u') {
          h = this.sched_time.getHours();
          m = this.sched_time.getMinutes();
        }
        this.sched_time = new Date(this.week_dates[i]);
        this.sched_time.setHours(h,m);
        // if (this.hour_selected != '') {
        //   this.sched_time.setHours(Number(this.hour_selected));
        // }
        this.sched_time_format = this.sched_time;
        this.sched_time_format = moment(this.sched_time_format).format('h:mm a (ddd, M/D)');
        console.log("i:",i,"date:",this.sched_time,this.week_dates[i],this.day_selected);
        this.session_type = 'u';
      }
    },

    hour_selected(newValue) { //when user selects hour
      var moment = require('moment');
      moment().format();
      if (this.sched_time == '' || this.session_type == 'p') { //use today by default
        this.sched_time = new Date();
        this.sched_time.setHours(0,0,0,0);
      }
      let h = Number(this.hour_selected);
      let m = this.sched_time.getMinutes();
      if (this.ap_selected == 'PM' && h < 12) { //add 12 hours for PM
        h += 12;
      }
      this.sched_time.setHours(h);
      this.sched_time_format = this.sched_time;
      this.sched_time_format = moment(this.sched_time_format).format('h:mm a (ddd, M/D)');
      console.log("time:",this.sched_time_format,this.sched_time,"h:",h,"m:",m);
      this.session_type = 'u';
    },

    min_selected(newValue) { //when user selects min
      var moment = require('moment');
      moment().format();
      if (this.sched_time == '' || this.session_type == 'p') { //use today by default
        this.sched_time = new Date();
        this.sched_time.setHours(0,0,0,0);
      }
      let h = this.sched_time.getHours();
      let m = 0;
      if (this.min_selected == '30') { //add 30 min if selected
        m = 30;
      }
      this.sched_time.setHours(h,m);
      this.sched_time_format = this.sched_time;
      this.sched_time_format = moment(this.sched_time_format).format('h:mm a (ddd, M/D)');
      console.log("time:",this.sched_time_format,this.sched_time,"h:",h,"m:",m);
       this.session_type = 'u';
    },

    ap_selected(newValue) { //when user selects AM or PM
      var moment = require('moment');
      moment().format();
      if (this.sched_time == '' || this.session_type == 'p') { //use today by default
        this.sched_time = new Date();
        this.sched_time.setHours(0,0,0,0);
      }
      let h = this.sched_time.getHours();
      let m = this.sched_time.getMinutes();
      if (this.ap_selected == 'PM' && h < 12) { //add 12 hours for PM
        h += 12;
      }
      else if (this.ap_selected == 'AM' && h >= 12) { //add 12 hours for PM
        h -= 12;
      }
      this.sched_time.setHours(h,m);
      this.sched_time_format = this.sched_time;
      this.sched_time_format = moment(this.sched_time_format).format('h:mm a (ddd, M/D)');
      console.log("time:",this.sched_time_format,this.sched_time,"h:",h,"m:",m);
       this.session_type = 'u';
    }
  },

  methods: {
    
    updateDaySched() {
      console.log('k');
    },

    onSubmit() {

      console.log('submit:',this.sched_time,this.time_current,(this.priv_selected) ? 1 : 0);
      if (this.sched_time != '' && this.time_current.getTime() < this.sched_time.getTime()) {

        //check if email is valid
        const re = /\S+@\S+\.\S+/;
        if (!re.test(this.user_email)) {
          alert("your email is invalid");
          return;
        }
        if (this.invite_email != '') { //invite friends
          let invite_email = this.invite_email.replace(/\s+/g, ''); //remove spaces
          let invite_emails = invite_email.split(',');
          console.log("friends:",invite_emails);
          for (let i in invite_emails) {
            if (!re.test(invite_emails[i])) {
              alert("invite emails are invalid");
              return;
            }  
          }
        }
        let duration = parseInt(this.user_duration);
        if (isNaN(duration) || duration < 5 || duration > 60 || duration % 5 > 0) {
          alert("set duration between 5 and 60 min in increments of 5 min");
          return;
        }

        this.submit_copy = 'Please check your email to confirm.'
        let sched_time_local = this.sched_time.toString();
        var entry = {
          user_id: this.user_id,
          user_email: this.user_email,
          sched_time: this.sched_time,
          session_type: this.session_type,
          sched_time_local: sched_time_local,
          session_hash: this.session_hash,
          invite_emails: this.invite_email,
          duration: duration,
          priv_bool: (this.priv_selected) ? 1 : 0
        };
        fetch('/api/schedsession', {
          method: "POST",
          body: JSON.stringify(entry),
          headers: new Headers({
          "content-type": "application/json"
          })
        })
        .then(response => {
          if (response.status !== 200) { //server error handling
            console.log(`Looks like there was a problem. Status code: ${response.status}`);
            return;
          }
          response.json().then(data => {

            console.log("session data:",data);
            if ('error' in data) { //error handling from backend call
              alert("schedule session error: " + data['error']);
              return;
            }

            if ('success' in data) { //inserted into sessions table
              console.log("session scheduled");
              this.refreshSessions(); //refresh session list
            }
          });
        })
        .catch(error => { //error handling
          console.log("Fetch error: " + error);
        });
      }
      else {
        alert("please pick a future time");
      }
    },

    onClaim(row) { //when user claims session

      this.session_type = 'p';
      this.sched_time = new Date(this.session_dates[row]);
      this.sched_time_format = this.sessions[row][1];
      this.session_hash = this.session_hashes[row];
      console.log("claim:",this.sched_time_format,this.session_hash);

      //loop sessions and uncolor all
      for (let i = 0; i < this.sessions.length; i++) {
        this.$refs['session_rows'][i].style.background = "#2AD9FF";
        console.log("unselected:",this.$refs['session_rows'][i]);
      }
      
      //change color of selected row
      this.$refs['session_rows'][row].style.background = '#18A0FB';
      console.log("selected:",this.$refs['session_rows'][row]);
    },

    refreshSessions() {
      
      fetch('/api/sessionlist')
      .then(response => {
        if (response.status !== 200) { //server error handling
          console.log(`Looks like there was a problem. Status code: ${response.status}`);
          return;
        }
        response.json().then(data => {

          console.log("session list data:",data);
          if ('error' in data) { //error handling from backend call
            alert("session list error: " + data['error']);
            return;
          }
          //row: session_id, user_id, user_email, sched_time, session_hash
          if (Array.isArray(data)) { //data is sessions table
            this.sessions = [];
            this.session_hashes = [];
            this.session_dates = [];
            var moment = require('moment');
            moment().format();
            for (let i = 0; i < data.length; i++) {

              //stores session hash
              let data_row = data[i];
              let session_hash = data_row.pop();
              this.session_hashes.push(session_hash);

              //array with sched date objects
              let sched_date = new Date(data_row[3]);
              //console.log("sesh:",this.sessions[i][3],sched_date);
              this.session_dates.push(sched_date);

              //formatting sched time field for UI
              sched_date = moment(sched_date).format('h:mm a (ddd, M/D)');
              data_row[3] = sched_date;

              let data_row_new = []; //clean data for each row
              data_row_new.push(data_row[2]);
              data_row_new.push(data_row[3]);
              data_row_new.push('15 min');

              this.sessions.push(data_row_new);
              console.log("data_row",data_row,"data_row_new",data_row_new);
            }
            console.log("sessions:",this.sessions);
          }
        });
      })
      .catch(error => { //error handling
        console.log("Fetch error: " + error);
      });
    },

    confirmSched(session) {

      let sched_time_local = this.sched_time.toString();

      var entry = {
        user_id: this.user_id,
        user_email: this.user_email,
        sched_time: this.sched_time,
        session_type: session,
        session_id: this.session_id,
        sched_time_local: sched_time_local
      };

      fetch('/api/schedconfirm', {
        method: "POST",
        body: JSON.stringify(entry),
        headers: new Headers({
        "content-type": "application/json"
        })
      })
      .then(response => {
        if (response.status !== 200) { //server error handling
          console.log(`Looks like there was a problem. Status code: ${response.status}`);
          return;
        }
        response.json().then(data => {

          console.log("sched data:",data);
          if ('error' in data) { //error handling from backend call
            alert("sched error: " + data['error']);
            return;
          }
          console.log("status:",data['success']);
        });
      })
      .catch(error => { //error handling
        console.log("Fetch error: " + error);
      });      
    }
  }
}
</script>


<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

html, body {
  height: 100%;
  margin: 0;
}

.waiting-room {
  /*font-family: 'DIN Condensed', sans-serif;*/
  font-size: 20px;
  background-color:#2AD9FF;
  color:#FFFFFF;
  line-height: 1.5;
  /*height: 100%;
  width: 100%;*/
  position: absolute;
  top: 0;
  bottom: 0;
  left: 0;
  right: 0;
}

.session-table {
  display: table;

  margin-left: auto;
  margin-right: auto;
}

.session-headers {
  display: table-row;
  font-weight: bold;
  text-align: center;
}

.session-cells {
  display: table-cell;
  border: solid;
  border-width: thin;
}

.session-rows {
  display: table-row;
}

.test-session-button {
  font-size: 18px;
  border-radius: 6px;
  border: 1px solid #18A0FB;
  /*
  font-family: 'DIN Condensed', sans-serif;
  padding-top: 10px;
  padding-bottom: 10px;
  padding-right: 40px;
  padding-left: 40px;
  */
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
