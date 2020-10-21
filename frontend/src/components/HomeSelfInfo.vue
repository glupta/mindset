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
            <p class="today">TODAY</p>
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
          <div class="home-dateactive">
            <p class="thu">Thu</p>
            <p class="num-24">24</p>
            <div class="oval"></div>
          </div>
          <div class="home-dateinactive">
            <p class="fri">Fri</p>
            <p class="num-25">25</p>
            <div class="oval-copy-7"></div>
          </div>
          <div class="home-dateinactive">
            <p class="fri">Sat</p>
            <p class="num-25">26</p>
            <div class="oval-copy-7"></div>
          </div>
          <div class="home-dateinactive">
            <p class="fri">Sun</p>
            <p class="num-25">27</p>
            <div class="oval-copy-7"></div>
          </div>
          <div class="home-dateinactive">
            <p class="fri">Mon</p>
            <p class="num-25">28</p>
            <div class="oval-copy-7"></div>
          </div>
          <div class="home-dateinactive">
            <p class="fri">Tue</p>
            <p class="num-25">29</p>
            <div class="oval-copy-7"></div>
          </div>
          <div class="home-dateinactive">
            <p class="fri">Wed</p>
            <p class="num-25">30</p>
            <div class="oval-copy-7"></div>
          </div>
        </div>
        
        
      </div>
      <div class="oval-copy-8"></div>
      <div class="oval-copy-9"></div>
      <div class="oval-copy-10"></div>
    </div>
    <div class="label-newcategory-action">
      <p class="daily-goal">DAILY GOAL</p>
      <p class="edit">EDIT</p>
    </div>
    <div class="home-progressbar">
      <div class="full-bar"></div>
      <div class="rectangle-bar"></div>
    </div>
    <!--HomeProgressChart class="home-progresschart"></HomeProgressChart-->
    <div class="home-habitssegcontrol">
      <p class="option1">MY HABITS</p>
      <p class="option2">PARTNER HABITS</p>
    </div>
    <div class="label-newcategory-action">
      <p class="daily-goal">DAILY GOAL</p>
      <p class="edit">EDIT</p>
    </div>
    <div class="flex-wrapper1">
      <HomeWellnessCard class="home-myhabits-wellnesshabit-card">        
      </HomeWellnessCard>
      <HomeWellnessCard class="home-myhabits-wellnesshabit-card">
      </HomeWellnessCard>
    </div>
  </div>
</template>

<script>
import router from '@/router'
import HomeWellnessCard from '@/components/HomeWellnessCard'
export default {
  name: "HomeSelfInfo",
  components: {
    HomeWellnessCard
  },
  data () {
    return {

    }
  },
  mounted() {

    //check cookie to stay logged in
    if (this.$cookies.isKey('mindset')) {
      let cookie_obj = this.$cookies.get('mindset');
      if (cookie_obj.hasOwnProperty('session_hash')) {
        this.session_hash = cookie_obj.session_hash;
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
            else if ('habit_bool' in data) {
              console.log("logged in:",data);
              if (data['habit_bool'] == 0) {
                console.log("no habits:",data['habit_bool']);
                router.push({ name: "SignUpHabit" });
              }
            }
            else {
              router.push({ name: "Home4" });
            }
          });
        })
        .catch(error => { //error handling
          console.log("Fetch error: " + error);
        });
      }
    }
    else {
      router.push({ name: "Home4" });
    }
  },
  methods: {
    onLogOut() {
      let obj_remove = this.$cookies.remove('mindset');
      router.push({ name: "Home4" });
    }
  }
};
</script>

<style scoped>
.iphone-11-pro-max-copy-12 {
  padding: 0px 0px 74px;
  display: flex;
  flex-direction: column;
  align-items: center;
}
.relative-wrapper2 {
  display: flex;
  align-items: flex-start;
  position: relative;
}
.rectangle {
  width: 412px;
  height: 67px;
  background-color: rgba(216, 216, 216, 1);
  position: absolute;
  left: 0px;
  top: 0px;
  border: 1px solid rgba(151, 151, 151, 1);
}
.group {
  padding: 44px 121px 4px;
  display: flex;
  align-items: flex-start;
  position: relative;
  background-image: url("https://static.overlay-tech.com/assets/b1656de2-836d-4805-a2ba-ee0832a9391e.png");
}
.mocktemplate {
  width: 172px;
  height: 20px;
  background-color: rgba(246, 247, 248, 1);
}
.group-2 {
  display: flex;
  flex-direction: row;
  align-items: center;
  position: absolute;
  right: 150px;
  bottom: 5px;
}
.img-5149 {
  width: 7px;
  height: 10px;
  margin-right: 7px;
}
.mindset-ooo {
  font-family: "SF Pro";
  font-size: 14px;
  font-weight: 500;
  line-height: normal;
  color: rgba(40, 40, 40, 1);
  text-align: center;
  letter-spacing: 2px;
}
.relative-wrapper1 {
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
/*
.flex-wrapper1 {
  padding: 0px 0px 0px 25px;
  display: flex;
  flex-direction: row;
  align-items: flex-start;
}
*/
.home-myhabits-wellnesshabit-card {
  &:not(:last-of-type) {
    margin-right: 15px;
  }
}

/* header today */
.header-today {
  background-color: rgba(255, 255, 255, 1);
  border-radius: 20px 20px 0 0;
  padding: 9px 24px 16px 19px;
  box-shadow: 0px -3px 6px 0px rgba(156, 156, 156, 0.31);
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  border: 1px solid rgba(54, 69, 135, 0.11);
}
.flex-wrapper1 {
  width: 454px;
  margin-right: 14px;
  padding: 10px 0px 0px;
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
  margin-right: 14px;
  display: flex;
  flex-direction: column;
  align-items: center;
}
.today {
  width: 116px;
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
  padding: 8px 0px 0px;
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
.home-dateactive {
  padding: 0px 0px 28px;
  display: flex;
  align-items: flex-start;
  position: relative;
  margin-left: 5px;
}
.thu {
  width: 64px;
  font-family: "Catamaran";
  font-size: 16px;
  font-weight: 400;
  line-height: normal;
  color: rgba(37, 49, 85, 1);
  text-align: center;
  position: absolute;
  left: 0px;
  bottom: 3px;
  letter-spacing: 2px;
}
.num-24 {
  width: 64px;
  font-family: "Source Sans Pro";
  font-size: 24px;
  font-weight: 600;
  line-height: normal;
  color: rgba(37, 49, 85, 1);
  text-align: center;
  position: relative;
  letter-spacing: 2px;
}
.oval {
  width: 4px;
  height: 4px;
  background-color: rgba(37, 49, 85, 1);
  border-radius: 50%;
  position: absolute;
  left: 30px;
  bottom: 0px;
}

/* date inactive */
.home-dateinactive {
  padding: 0px 0px 28px;
  display: flex;
  align-items: flex-start;
  position: relative;
}
.fri {
  width: 64px;
  font-family: "Catamaran";
  font-size: 16px;
  font-weight: 400;
  line-height: normal;
  color: rgba(39, 49, 77, 1);
  text-align: center;
  opacity: 0.2;
  position: absolute;
  left: 0px;
  bottom: 3px;
  letter-spacing: 2px;
}
.num-25 {
  width: 64px;
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
.oval-copy-7 {
  width: 4px;
  height: 4px;
  border-radius: 50%;
  position: absolute;
  left: 30px;
  bottom: 0px;
}

/* icon calendar */
.icon-calendar {
  padding: 0px 1px 0px 0px;
  display: flex;
  align-items: flex-start;
  margin-bottom: 20px;
  margin-left: 17px;
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
  margin-bottom: 8px;
  margin-left: 25px;
}
.daily-goal {
  font-family: "Catamaran";
  font-size: 14px;
  font-weight: 200;
  line-height: normal;
  color: rgba(38, 49, 82, 1);
  text-transform: uppercase;
  margin-right: 242px;
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
}

/* progress bar */
.home-progressbar {
  padding: 0px 0px 1px;
  display: flex;
  align-items: flex-start;
  position: relative;
  margin-bottom: 16px;
  margin-left: 24px;
}
.full-bar {
  width: 364px;
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
  margin-bottom: 16px;
  margin-left: 25px;
}
.option1 {
  font-family: "Catamaran";
  font-size: 18px;
  font-weight: 700;
  line-height: normal;
  color: rgba(37, 49, 85, 1);
  margin-right: 32px;
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
}
</style>