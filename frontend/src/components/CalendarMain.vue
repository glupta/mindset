<template>
  <div class="calendar-main">
    <div class="calendar">
      <p class="current-month">{{current_month}}</p>
      <div class="daysoftheweek-title">
        <div v-for="(day,n) of week_days" class="weekdays">
          <p class="weekdaytext">{{day}}</p>
        </div>
      </div>
      <div class="flex-wrapper1">
        <!--img class="icons-chevron-left" src="https://via.placeholder.com/24x24"/-->
        <div class="calendar-dates">
          <div v-for="(date,n) of week_dates" class="date-cell">
            <div class="calendar-day">
              <div v-if="n!=date_active" class="day-inactive" @click="onSelectDate(n)">
                <p class="day-text-inactive">{{date}}</p>
              </div>
              <div v-if="n==date_active" class="day-active">
                <div class="date-indicator">
                  <div class="oval">
                    <p class="day-text-active">{{date}}</p>
                  </div>
                </div>
                <img class="day-border" src="https://static.overlay-tech.com/assets/271f5aeb-5d3e-4c63-9167-32e46ba0f748.png"/>
              </div>
            </div>
          </div>
        </div>
        <!--img class="icons-chevron-right" src="https://via.placeholder.com/24x24"/-->
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "CalendarMain",
  data () {
    return {
      current_month: '',
      date_active: 0,
      week: [],
      week_days: [],
      week_dates: [],
      hours: []
    }
  },
  mounted() {
    fetch('/api/timedata') //get current datetime
    .then(response => {
      if (response.status !== 200) { //server error handling
        console.log(`Looks like there was a problem. Status code: ${response.status}`);
        return;
      }
      response.json().then(data => {

        console.log("time data:",data);
        if ('error' in data) { //error handling from testroom backend call
          console.log("request time error: ",data['error']);
          alert("request time error: " + data['error']);
          return;
        }
        
        var moment = require('moment');
        moment().format();

        //get today's date
        this.time_current = new Date(data['time_current']);
        let today = new Date(this.time_current.getFullYear(),this.time_current.getMonth(),this.time_current.getDate());
        let today_month = today;
        this.current_month = moment(today_month).format('MMM')

        for (let i = 0; i < 7; i++) { //find next 6 days in weeks

          let today_day = today;
          let today_date = today;
          let today_str = today.toString();
          this.week.push(today_str);
          this.week_days.push(moment(today_day).format('ddd'));
          this.week_dates.push(moment(today_date).format('D'));
          //console.log("today:",today,"day:",today_day,"date:",today_date);
          today.setDate(today.getDate() + 1);
        }

        console.log("current:",this.time_current,"today:",today);
        console.log("week:",this.week,"weekdays:",this.week_days,"weekdates:",this.week_dates);
      });
    })
    .catch(error => { //error handling
      console.log("Fetch error: " + error);
    });
  },
  methods: {
    onSelectDate(n) {
      this.date_active = n;
      this.$emit('date-active',n);
    }
  }
};
</script>

<style scoped>
.calendar-main {
  padding: 0px 0px 2px;
  display: flex;
  align-items: flex-start;
}
.calendar {
  display: flex;
  flex-direction: column;
  align-items: center;
}
.calendar-dates {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
}
.current-month {
  width: 147px;
  font-family: "Source Sans Pro";
  font-size: 24px;
  font-weight: 700;
  line-height: 36px;
  color: rgba(66, 62, 61, 1);
  text-align: center;
  text-transform: uppercase;
  margin-bottom: 19px;
  letter-spacing: 3px;
}
.flex-wrapper1 {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  width: 1316px;
}
.date-cell {
  margin: 0 1px;
  width: 186px;
  height: 104px;
  cursor: pointer;
}
.day-inactive {
  background-color: rgba(220, 213, 187, 0.3);
  padding: 20px 20px 45px 126px;
}
.day-active {
  position: relative;
  left: 0;
  top: 0;
}
.date-indicator {
  display: flex;
  align-items: flex-start;
  position: relative;
  left: 134px;
  top: 26px;
}
.oval {
  width: 38px;
  height: 38px;
  border-radius: 50%;
  position: absolute;
  background-color: #FF0000
}
.day-text-inactive {
  font-family: "Source Sans Pro";
  font-size: 18px;
  font-weight: 600;
  line-height: 27px;
  color: rgba(66, 62, 61, 1);
  text-align: center;
  text-transform: uppercase;
  opacity: 0.3;
  position: relative;
  left: 8px;
  top: 6px;
  letter-spacing: 1px;
}
.day-text-active {
  font-family: "Source Sans Pro";
  font-size: 18px;
  font-weight: 600;
  line-height: 27px;
  color: #FFFFFF;
  text-align: center;
  text-transform: uppercase;
  position: absolute;
  left: 8px;
  top: 5px;
  letter-spacing: 1px;
}
.day-border {
  position: relative;
  left: 0;
  top: 0;
}
.icons-chevron-left {
  width: 24px;
  height: 24px;
}
.icons-chevron-right {
  width: 24px;
  height: 24px;
}

.daysoftheweek-title {
  display: flex;
  flex-direction: row;
  align-items: flex-start;
  margin-bottom: 7px;
}
.weekdays {
  background-color: rgba(250, 251, 251, 1);
  padding: 8px 0px 5px;
  width: 186px;
  display: flex;
  align-items: flex-start;
  margin: 0 1px;
}
.weekdaytext {
  width: 186px;
  font-family: "Source Sans Pro";
  font-size: 18px;
  font-weight: 600;
  line-height: 27px;
  color: rgba(66, 62, 61, 1);
  text-align: center;
  text-transform: uppercase;
  letter-spacing: 1px;
}
</style>