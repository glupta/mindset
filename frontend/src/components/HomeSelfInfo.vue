<template>
  <div class="iphone-11-pro-max-copy-12">
    <div class="relative-wrapper1">
      <div class="header-today">
        <div class="flex-wrapper1">
          <div class="log-out" @click="onLogOut">
            <img
              alt="box"
              class="box"
              src="https://static.overlay-tech.com/assets/a0729bd1-8332-4ce2-8ebe-cdf29aae2699.svg"
            /><img
              alt="path"
              class="path1"
              src="https://static.overlay-tech.com/assets/c56e3dfa-ea8d-47a4-ade8-9819da93c200.svg"
            />
          </div>
          <div class="flex-wrapper2">
            <p class="today">{{cal_header}}</p>
            <div class="flex-wrapper4">
            </div>
          </div>
          <div class="flex-wrapper3">
            <div class="icon-calendar">
              <div class="calendar-day-fifteen">
                <img
                  alt="num-1"
                  class="num-1"
                  src="https://static.overlay-tech.com/assets/d1169236-2a39-4b32-bcdf-47f1898baaba.svg"
                />
                <img
                  alt="path"
                  class="path2"
                  src="https://static.overlay-tech.com/assets/8b8f1f40-8ce4-477a-81a5-d0a3dd30a84d.svg"
                />
              </div>
            </div>
          </div>
        </div>
        <div class="cal-row">
          <div v-for="(day,i) of cal_days" class="home-date" @click="onSelectDate(i)">
            <p v-if="selected_day==i" class="num-24">{{cal_dates[i]}}</p>
            <p v-if="selected_day==i" class="thu">{{day}}</p>
            <div v-if="selected_day==i" class="oval"></div>
            <p v-if="selected_day!=i" class="num-25">{{cal_dates[i]}}</p>
            <p v-if="selected_day!=i" class="fri">{{day}}</p>
          </div>
        </div>
        
        
      </div>
      <div class="oval-copy-8"></div>
      <div class="oval-copy-9"></div>
      <div class="oval-copy-10"></div>
    </div>
    <div class="label-newcategory-action">
      <p class="daily-goal">WEEKLY PROGRESS</p>
    </div>
    <div class="home-progressbar">
      <div class="full-bar"></div>
      <div class="rectangle-bar"></div>
    </div>
    <!--HomeProgressChart class="home-progresschart"></HomeProgressChart-->
    <div class="home-habitssegcontrol">
      <p class="option1" id="my-habits" @click="onSelectMyHabits">MY HABITS</p>
      <p class="option2" id="partner-habits" @click="onSelectPartnerHabits">PARTNER'S HABITS</p>
    </div>
    <div class="label-newcategory-action">
      <p class="daily-goal">DAILY TRACKER</p>
      <p v-if="!partner_bool" class="edit" @click="onSelectEdit">EDIT</p>
      <p v-if="partner_bool" class="edit" @click="onSelectCompare">COMPARE</p>
    </div>
    <div class="wellness-card">
      <HomeWellnessCard v-if="!edit_bool" :sessionHash="selected_hash" :dataEntry="today_bool" :selectedDate="selected_date"></HomeWellnessCard>
    </div>
    <div v-if="popup_bool" class="shadow"></div>
    <div v-if="edit_bool" class="popup-slidercontainer-edit">
      <div class="popup-sliderheader-edit">
        <div class="flex-wrapper1-edit">
          <p class="title-edit">EDIT HABITS</p>
          <img
            alt="icons-xmark"
            class="icons-xmark"
            src="https://static.overlay-tech.com/assets/08689fdc-2beb-4e94-a37d-66212dd4a5e1.svg"
            @click="onSelectExit"
          />
        </div>
        <p class="body-edit">
          Things come up in life - we get it. Adjust your goals to fit your
          lifestyle.
        </p>
      </div>
      <div class="signup-gh">
        <div class="rectangle-input"></div>
        <div class="userentry-form-empty">
          <p class="form-label-form">Habit #1</p>
          <input v-model="habit_input" class="entrybox-form">
        </div>
        <!--div class="flex-wrapper1">
          <div class="userentry-dropdown1">
            <div class="entrybox-dd"></div>
            <p class="entrytext-dd">Days</p>
            <p class="form-label-dd">Frequency</p>
            <div class="chevron">
              <img
                alt="path"
                class="path"
                src="https://static.overlay-tech.com/assets/802de8b9-4e36-43c7-9105-f13915886d3c.svg"
              />
            </div>
          </div>
          <div class="userentry-dropdown2">
            <div class="entrybox-dd"></div>
            <p class="entrytext-dd">Days</p>
            <p class="form-label-dd">Frequency</p>
            <div class="chevron">
              <img
                alt="path"
                class="path"
                src="https://static.overlay-tech.com/assets/802de8b9-4e36-43c7-9105-f13915886d3c.svg"
              />
            </div>
          </div>
        </div>
      </div>
      <div class="controls-pagination-dots-light-3-dots">
        <div class="center">
          <div class="controls-pagination-dots-x-light-page-dot dot-1"></div>
          <div class="controls-pagination-dots-x-light-page-dot dot-1"></div>
          <div class="controls-pagination-dots-x-light-page-dot"></div>
        </div-->
      </div>
      <p class="next" @click="onSelectSaveEdit">SAVE</p>
    </div>
    <div v-if="compare_bool" class="popup-slidercontainer-compare">
      <div class="popup-sliderheader-compare">
        <div class="flex-wrapper1-edit">
          <p class="title-edit">COMPARE HABITS</p>
          <img
            alt="icons-xmark"
            class="icons-xmark"
            src="https://static.overlay-tech.com/assets/08689fdc-2beb-4e94-a37d-66212dd4a5e1.svg"
            @click="onSelectExit"
          />
        </div>
        <p class="body-edit">
          Competition never hurt anyone. Check how you compare with your partner today!
        </p>
      </div>
      <div class="wellness-compare">
        <p class="habit-compare-text">MY HABITS</p>
        <HomeWellnessCard class="wellness-card-compare" :sessionHash="session_hash" :dataEntry="false" :selectedDate="selected_date">
        </HomeWellnessCard>
        <p class="habit-compare-text">PARTNER’S HABITS</p>
        <HomeWellnessCard class="wellness-card-compare" :sessionHash="partner_hash" :dataEntry="false" :selectedDate="selected_date">
        </HomeWellnessCard>
      </div>
    </div>
    <PairingPopup v-if="pairing_bool"></PairingPopup>
  </div>
</template>

<script>
import router from '@/router'
import HomeWellnessCard from '@/components/HomeWellnessCard'
import PairingPopup from '@/components/PairingPopup'
export default {
  name: "HomeSelfInfo",
  data () {
    return {
      partner_bool: false,
      popup_bool: false,
      edit_bool: false,
      compare_bool: false,
      session_hash: "",
      pairing_bool: false,
      partner_hash: "",
      selected_hash: "",
      habit_input: "",
      cal_days: ['Sun','Mon','Tue','Wed','Thu','Fri','Sat'],
      cal_dates: ['','','','','','',''],
      cal_dates_full: ['','','','','','',''],
      selected_day: -1,
      selected_date: '',
      cal_header: "TODAY",
      today_bool: true
    }
  },
  components: {
    HomeWellnessCard,
    PairingPopup
  },
  mounted() {

    console.log("screen width:",window.screen.width);


    //check cookie to stay logged in
    if (this.$cookies.isKey('mindset')) {
      let cookie_obj = this.$cookies.get('mindset');
      if (cookie_obj.hasOwnProperty('session_hash')) {
        this.session_hash = cookie_obj.session_hash;
        this.selected_hash = this.session_hash;
        fetch('/api/checkhash?h=' + this.session_hash)
        .then(response => {
          if (response.status !== 200) { //server error handling
            console.log(`Looks like there was a problem. Status code: ${response.status}`);
            let obj_remove = this.$cookies.remove('mindset');
            router.push({ name: "Home4" });
            return;
          }
          response.json().then(data => {
            if ('error' in data) {
              alert(data['error']);
              let obj_remove = this.$cookies.remove('mindset');
              router.push({ name: "Home4" });
            }
            else if ('habit_name' in data) {
              if (!data['habit_name']) {
                router.push({ name: "SignUpHabit" });
              }
              else if (!data['partner_hash']) {
                this.popup_bool = true;
                this.pairing_bool = true;
              }
              else {
                this.partner_hash = data['partner_hash'];
                this.habit_input = data['habit_name'];
                console.log("partner hash:",this.partner_hash);
              }
            }
          });
        })
        .catch(error => { //error handling
          console.log("Fetch error: " + error);
          router.push({ name: "Home4" });
        });
      }
    }
    else {
      router.push({ name: "Home4" });
    }

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

        //get today's date
        this.time_current = new Date(data['time_current']);
        this.selected_date = this.time_current;
        this.today_day = this.time_current.getDay();
        let today_date = this.time_current.getDate();
        this.selected_day = this.today_day;

        for (let i = 0; i < 7; i++) { //find next 6 days in current week
          const date = new Date();
          date.setDate(today_date - this.today_day + i);
          this.cal_dates_full[i] = date;
          this.cal_dates[i] = date.getDate();
        }
      });
    })
    .catch(error => { //error handling
      console.log("Fetch error: " + error);
    });
  },
  methods: {
    onLogOut() {
      let obj_remove = this.$cookies.remove('mindset');
      router.push({ name: "Home4" });
    },
    onSelectDate(selected_day) {

      this.selected_day = selected_day;
      this.selected_date = this.cal_dates_full[selected_day];
      this.today_bool = false;
      console.log("selected_date:",this.selected_date);

      if (selected_day == this.today_day) {
        if (this.partner_bool == false) {
          this.today_bool = true;
        }
        this.cal_header = "TODAY";
      }
      else if (selected_day == this.today_day - 1) {
        this.cal_header = "YESTERDAY";
      }
      else if (selected_day == this.today_day + 1) {
        this.cal_header = "TOMORROW";
      }
      else if (selected_day < this.today_day - 1) {
        this.cal_header = "EARLIER";
      }
      else if (selected_day > this.today_day + 1) {
        this.cal_header = "LATER";
      }
    },
    onSelectMyHabits() {
      document.getElementById("my-habits").className = "option1";
      document.getElementById("partner-habits").className = "option2";
      this.partner_bool = false;
      if (this.selected_day == this.today_day) {
        this.today_bool = true;
      }
      this.selected_hash = this.session_hash;
    },
    onSelectPartnerHabits() {
      document.getElementById("my-habits").className = "option2";
      document.getElementById("partner-habits").className = "option1";
      this.partner_bool = true;
      this.today_bool = false;
      this.selected_hash = this.partner_hash;
    },
    onSelectEdit() {
      this.popup_bool = true;
      this.edit_bool = true;
    },
    onSelectCompare() {
      this.popup_bool = true;
      this.compare_bool = true;
    },
    onSelectExit() {
      this.popup_bool = false;
      this.edit_bool = false;
      this.compare_bool = false;
    },
    onSelectSaveEdit() {
      //update habit in DB
      if (this.habit_input == '') {
        alert("Oops! Something went wrong. Please enter a habit.");
      }
      else if (this.habit_input.length > 30) {
        alert("Oops! Something went wrong. Please shorten your habit.");
      }
      else {
        var entry = {
          session_hash: this.session_hash,
          habit_name: this.habit_input
        };
        fetch('/api/newhabit', {
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
            if ('error' in data) {
              alert(data['error']);
            }
            else if ('success' in data) { //refresh wellness card
              this.popup_bool = false;
              this.edit_bool = false;
            }
            else {
              alert("Oops! Something went wrong. Please enter your habit again.")
            }
          });
        })
        .catch(error => { //error handling
          console.log("Fetch error: " + error);
        });
      }
    }
  }
};
</script>

<style scoped>

.iphone-11-pro-max-copy-12 {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
}
.relative-wrapper1 {
  width: 375px;
  margin-bottom: 32px;
  display: flex;
  align-items: flex-start;
  position: relative;
}
.oval-copy-8 {
  width: 4px;
  height: 4px;
  border-radius: 50%;
  position: absolute;
  left: 205px;
  bottom: 13px;
}
.oval-copy-9 {
  width: 4px;
  height: 4px;
  border-radius: 50%;
  position: absolute;
  right: 130px;
  bottom: 13px;
}
.oval-copy-10 {
  width: 4px;
  height: 4px;
  border-radius: 50%;
  position: absolute;
  right: 55px;
  bottom: 13px;
}
.home-progresschart {
  margin-bottom: 32px;
  margin-left: 24px;
}
.home-myhabits-wellnesshabit-card {
  &:not(:last-of-type) {
    margin-right: 15px;
  }
}

/* header today */
.header-today {
  background-color: rgba(255, 255, 255, 1);
  border-radius: 20px 20px 0 0;
  padding: 8px 16px 16px 16px;
  box-shadow: 0px -3px 6px 0px rgba(156, 156, 156, 0.31);
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  border: 1px solid rgba(54, 69, 135, 0.11);
  width: 100%;
}
.flex-wrapper1 {
  width: calc(100%-28px);
  padding: 10px 14px 0px 14px;
  display: flex;
  flex-direction: row;
  align-items: flex-start;
  justify-content: space-between;
}
.icon-logout {
  margin-bottom: 22px;
}
.header-today-date1-copy {
  margin-left: 5px;
}
.header-today-dateinactive-copy-4 {
  margin-top: 52px;
  margin-right: 14px;
}
.flex-wrapper2 {
  width: 100%;
  display: flex;
  flex-direction: column;
  text-align: center;
  justify-content: center;
}
.today {
  font-family: "Catamaran";
  font-size: 24px;
  font-weight: 500;
  line-height: normal;
  color: rgba(65, 67, 68, 1);
  text-align: center;
  margin-bottom: 12px;
  letter-spacing: 2px;
}
.flex-wrapper4 {
  display: flex;
  flex-direction: row;
  align-items: flex-start;
}
.header-today-dateinactive-copy-7 {
  &:not(:last-of-type) {
    margin-right: 14px;
  }
}
.header-today-dateinactive-copy-6 {
  margin-right: 13px;
}
.flex-wrapper3 {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}
.cal-row {
  display: flex;
  flex-direction: row;

}

/* log out */
.log-out {
  padding: 0px 0px 0px 9px;
  display: flex;
  align-items: flex-start;
  position: relative;
  margin-bottom: 22px;
  cursor: pointer;
}
.box {
  width: 13px;
  height: 20px;
  position: relative;
}
.path1 {
  width: 17px;
  height: 9px;
  position: absolute;
  left: 0px;
  top: 5px;
}

/* date active */
.home-date {
  display: flex;
  flex-direction: column;
  align-items: center;
  cursor: pointer;
}
.num-24 {
  width: 48px;
  height: 30px;
  font-family: "Source Sans Pro";
  font-size: 24px;
  font-weight: 600;
  line-height: normal;
  color: rgba(37, 49, 85, 1);
  text-align: center;
  letter-spacing: 2px;
}
.thu {
  width: 48px;
  height: 28px;
  font-family: "Catamaran";
  font-size: 16px;
  font-weight: 400;
  line-height: normal;
  color: rgba(37, 49, 85, 1);
  text-align: center;
  letter-spacing: 2px;
}
.oval {
  width: 4px;
  height: 4px;
  background-color: rgba(37, 49, 85, 1);
  border-radius: 50%;
}

/* date inactive */
.num-25 {
  width: 48px;
  height: 30px;
  font-family: "Source Sans Pro";
  font-size: 24px;
  font-weight: 600;
  line-height: normal;
  color: rgba(39, 49, 77, 1);
  text-align: center;
  opacity: 0.2;
  position: relative;
  letter-spacing: 2px;
}
.fri {
  width: 48px;
  height: 28px;
  font-family: "Catamaran";
  font-size: 16px;
  font-weight: 400;
  line-height: normal;
  color: rgba(39, 49, 77, 1);
  text-align: center;
  opacity: 0.2;
  letter-spacing: 2px;
}
.oval-copy-7 {
  width: 4px;
  height: 4px;
  border-radius: 50%;
  position: absolute;
}

/* icon calendar */
.icon-calendar {
  display: flex;
  align-items: flex-start;
}
.calendar-day-fifteen {
  padding: 10px 6px 4px;
  display: flex;
  flex-direction: row;
  align-items: flex-start;
  background-image: url("https://static.overlay-tech.com/assets/d64ad787-259e-4c2c-959e-f4c0e4e407ce.png");
}
.num-1 {
  width: 3px;
  height: 10px;
  margin-right: 3px;
}
.path2 {
  width: 5px;
  height: 10px;
}

/* label new category */
.label-newcategory-action {
  display: flex;
  flex-direction: row;
  align-items: flex-start;
  justify-content: space-between;
  margin-bottom: 16px;
  margin-left: 24px;
  margin-right: 24px;
  width: 352px;
}
.daily-goal {
  font-family: "Catamaran";
  font-size: 14px;
  font-weight: 200;
  line-height: normal;
  color: rgba(38, 49, 82, 1);
  text-transform: uppercase;
  opacity: 0.7;
  letter-spacing: 1px;
}
.edit {
  font-family: "Catamaran";
  font-size: 14px;
  font-weight: 600;
  line-height: normal;
  color: rgba(38, 49, 82, 1);
  text-align: right;
  letter-spacing: 2px;
  cursor: pointer;
}

/* progress bar */
.home-progressbar {
  padding: 0px 0px 1px;
  display: flex;
  align-items: flex-start;
  position: relative;
  margin-bottom: 16px;
}
.full-bar {
  width: 352px;
  height: 10px;
  background-color: rgba(237, 237, 237, 1);
  border-radius: 12px;
  position: relative;
}
.rectangle-bar {
  width: 257px;
  height: 10px;
  border-radius: 12px;
  box-shadow: 2px 3px 5px 0px rgba(67, 67, 67, 0.15);
  background: linear-gradient(
    89deg,
    rgba(37, 49, 85, 1) -5%,
    rgba(76, 95, 142, 1) 93%
  );
  position: absolute;
  left: 0px;
  bottom: 0px;
}

/* segment control */
.home-habitssegcontrol {
  display: flex;
  flex-direction: row;
  align-items: flex-start;
  justify-content: space-between;
  margin-bottom: 16px;
  margin-left: 24px;
  margin-right: 24px;
  width: 352px;
}
.option1 {
  font-family: "Catamaran";
  font-size: 18px;
  font-weight: 700;
  line-height: normal;
  color: rgba(37, 49, 85, 1);
  letter-spacing: 2px;
}
.option2 {
  font-family: "Catamaran";
  font-size: 18px;
  font-weight: 400;
  line-height: normal;
  color: rgba(37, 49, 85, 1);
  opacity: 0.3;
  letter-spacing: 2px;
  cursor: pointer;
}

/* wellness cards */
.wellness-card {
  width: 350px;
  padding: 10px 14px 0px 14px;
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
}

/* edit habits */
.shadow {
  width: 375px;
  height: 100%;
  background-color: rgba(149, 149, 149, 1);
  opacity: 0.85;
  box-shadow: 0px -1px 3px 0px rgba(0, 0, 0, 0.15);
  position: absolute;
}
.popup-slidercontainer-edit {
  border-radius: 15px 15px 0 0;
  box-shadow: 0px -3px 7px 0px rgba(52, 52, 52, 0.23);
  display: flex;
  flex-direction: column;
  align-items: center;
  background: linear-gradient(
    161deg,
    rgba(245, 247, 250, 1) 35%,
    rgba(245, 247, 250, 1) 100%
  );
  border: 1px solid rgba(54, 69, 135, 0.11);
  position: absolute;
  width: 373px;
  top: 160px;
  bottom: 0px;
}
.popup-sliderheader-edit {
  background-color: rgba(255, 255, 255, 1);
  border-radius: 20px 20px 0 0;
  padding: 24px 16px 16px 16px;
  box-shadow: 0px 3px 6px 0px rgba(156, 156, 156, 0.31);
  display: flex;
  flex-direction: column;
  align-items: center;
  width: calc(100%-32px);
  margin-bottom: 32px;
}
.flex-wrapper1-edit {
  margin-bottom: 6px;
  padding: 0 16px 0 16px;
  display: flex;
  flex-direction: row;
  align-items: flex-start;
  justify-content: space-between;
  width: calc(100%-32px);
}
.title-edit {
  font-family: "Catamaran";
  font-size: 18px;
  font-weight: 600;
  line-height: normal;
  color: rgba(38, 49, 82, 1);
  letter-spacing: 2px;
}
.body-edit {
  width: 346px;
  font-family: "Catamaran";
  font-size: 16px;
  font-weight: 400;
  line-height: 24px;
  color: rgba(37, 49, 85, 1);
  opacity: 0.7;
  letter-spacing: 1px;
}
.icons-xmark {
  width: 24px;
  height: 24px;
  cursor: pointer;
}

.next {
  width: 100px;
  font-family: "Source Sans Pro";
  font-size: 16px;
  font-weight: 600;
  line-height: 24px;
  color: rgba(37, 49, 85, 1);
  text-align: center;
  text-decoration: underline;
  letter-spacing: 2px;
  cursor: pointer;
}

.signup-gh {
  background-color: rgba(255, 255, 255, 1);
  border-radius: 0 0 15px 15px;
  padding: 0px 0px 17px;
  box-shadow: 0px 3px 6px 0px rgba(0, 0, 0, 0.06);
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  border: 1px solid rgba(151, 151, 151, 0.16);
  margin-bottom: 8px;
}

.rectangle-input {
  width: 329px;
  height: 16px;
  background-color: rgba(247, 195, 79, 1);
  margin-bottom: 16px;
  margin-left: -1px;
}

.userentry-form-empty {
  padding: 22px 0px 0px;
  display: flex;
  align-items: flex-start;
  position: relative;
  margin-bottom: 24px;
  margin-left: 24px;
}
.entrybox-form {
  width: 263px;
  height: 38px;
  background-color: rgba(255, 255, 255, 1);
  border-radius: 8px;
  position: relative;
  border: 1px solid rgba(37, 49, 85, 0.3);
  padding-left: 8px;
}

::placeholder {
  font-family: "Catamaran";
  font-size: 16px;
  font-weight: 400;
  line-height: 24px;
  color: rgba(37, 49, 85, 1);
  opacity: 0.7;
  letter-spacing: 1px;
}

.entrytext-form {
  width: 255px;
  font-family: "Catamaran";
  font-size: 16px;
  font-weight: 400;
  line-height: 24px;
  color: rgba(37, 49, 85, 1);
  opacity: 0.7;
  position: absolute;
  right: 0px;
  bottom: 8px;
  letter-spacing: 1px;
}
.form-label-form {
  width: 261px;
  font-family: "Catamaran";
  font-size: 14px;
  font-weight: 200;
  line-height: normal;
  color: rgba(38, 49, 82, 1);
  text-transform: uppercase;
  opacity: 0.7;
  position: absolute;
  right: 0px;
  top: 0px;
  letter-spacing: 1px;
}

/* compare */
.popup-slidercontainer-compare {
  border-radius: 15px 15px 0 0;
  box-shadow: 0px -3px 7px 0px rgba(52, 52, 52, 0.23);
  display: flex;
  flex-direction: column;
  align-items: center;
  background: linear-gradient(
    161deg,
    rgba(245, 247, 250, 1) 35%,
    rgba(245, 247, 250, 1) 100%
  );
  border: 1px solid rgba(54, 69, 135, 0.11);
  position: absolute;
  width: 373px;
  top: 100px;
  bottom: 0px;
}
.popup-sliderheader-compare {
  background-color: rgba(255, 255, 255, 1);
  border-radius: 20px 20px 0 0;
  padding: 24px 16px 16px 16px;
  box-shadow: 0px 3px 6px 0px rgba(156, 156, 156, 0.31);
  display: flex;
  flex-direction: column;
  align-items: center;
  width: calc(100%-32px);
  margin-bottom: 32px;
}
.wellness-compare {
  width: calc(100%-28px);
  padding: 10px 14px 0px 14px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}
.habit-compare-text {
  font-family: "Catamaran";
  font-size: 14px;
  font-weight: 200;
  line-height: normal;
  color: rgba(38, 49, 82, 1);
  text-transform: uppercase;
  opacity: 0.7;
  letter-spacing: 1px;
  margin-bottom: 8px;
}
.wellness-card-compare {
  margin-bottom: 32px;
}
</style>