<template>
  <div class="newsession">
    <div class="newsession-headertext">
      <p class="new-session">NEW SESSION</p>
      <p class="rooms-open-5-minutes">
        Rooms open 5 minutes before the start of the scheduled session.
      </p>
    </div>
    <div class="flex-wrapper1">
      <div class="flex-wrapper3">
        <div class="newsession-starttime">
          <p class="start-time">START TIME:</p>

          <div class="schedule-starttime schedule-new-starttime">
            <div class="group-6">
              <div class="hour" @click="hour_bool=true">
                <p class="num-12">{{hour_selected}}</p>
                <img class="icons-chevron-down" src="@/assets/img/chevron-down.svg"/>
              </div>

              <div v-if="hour_bool" class="dropdownboundarybox-hr">
                <div v-for="n in 12" class="flex-wrapper-hour" @mouseover="hour_hover=n" @mouseleave="hour_hover=0" @click="onSelectHour(n)">
                  <p class="num-1">{{n}}</p>
                  <div v-if="hour_hover==n" class="icons-checkmark">
                    <img class="icons-check" src="https://static.overlay-tech.com/assets/a4e1e936-e529-4502-a4a0-ae912dfc83d0.png"/>
                  </div>
                </div>
              </div>

              <div class="hour2" @click="min_bool=true">
                <p class="num-12">{{min_selected}}</p>
                <img class="icons-chevron-down" src="@/assets/img/chevron-down.svg"/>
              </div>

              <div v-if="min_bool" class="dropdownboundarybox-min">
                <div v-for="(min,n) of mins" class="flex-wrapper-min" @mouseover="min_hover=n" @mouseleave="min_hover=-1" @click="onSelectMin(n)">
                  <p class="num-00">{{min}}</p>
                  <div v-if="min_hover==n" class="icons-checkmark">
                    <img class="icons-check" src="https://static.overlay-tech.com/assets/a4e1e936-e529-4502-a4a0-ae912dfc83d0.png"/>
                  </div>
                </div>
              </div>

            </div>
            <div class="oval"></div>
            <div class="oval-copy"></div>
          </div>


          <div class="ampm-toggle">

            <div v-if="am_bool==true" class="group-5">
              <div class="am-highlight active-highlight">
                <div class="underline1"></div>
              </div>
              <p class="am1">AM</p>
            </div>
            <p v-if="am_bool==true" class="pm1" @click="am_bool=false">PM</p>

            <div v-if="am_bool==false" class="group-6">
              <div class="amreactive">
                <p class="am2" @click="am_bool=true">AM</p>
              </div>
              <div class="relative-wrapper1">
                <div class="selectedhighlight"></div>
                <div class="underline2"></div>
                <p class="pm2">PM</p>
              </div>
            </div>

          </div>

        </div>

        <div class="newsession-duration">
          <p class="duration">DURATION:</p>

          <input v-model="user_duration" class="entry-totaldurationmin input"/>

          <p class="minutes">minutes</p>
        </div>
      </div>
      <div class="flex-wrapper3">
        <p class="invite-friend">INVITE FRIEND:</p>

        <input v-model="invite_email" class="invite-friend-input input" placeholder="Recipient's email" />

      </div>
    </div>
    <div class="flex-wrapper2">

      <div class="group-2">

        <div :class="{'selected-rec':priv_bool, unselected:!priv_bool}" @click="priv_bool=!priv_bool"></div>

        <p class="private">Private</p>

        <img @click="onSelectPrivInfo" class="icons-info" src="@/assets/img/info.svg"/>

      </div>

      <div @click="onNewConfirm" class="button-dark">
        <p class="confirm">CONFIRM</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "NewSession",
  data () {
    return {
      am_bool: true,
      hour_bool: false,
      hour_hover: 0,
      hour_selected: 12,
      min_bool: false,
      min_hover: -1,
      min_selected: '00',
      mins: ['00','15','30','45'],
      user_duration: 15,
      invite_email: '',
      priv_bool: false
    }
  },
  props: [
    'dateActive'
  ],
  methods: {
    onSelectHour(n) {
      this.hour_bool = false;
      this.hour_selected = n;
    },
    onSelectMin(n) {
      this.min_bool = false;
      this.min_selected = this.mins[n];
    },
    onSelectPrivInfo() {
      this.$emit("priv-info");
    },
    onNewConfirm() {
      this.sched_time = new Date(this.dateActive);
      let h = Number(this.hour_selected);
      if (this.am_bool == true && h == 12) {
        h = 0;
      }
      else if (this.am_bool == false && h < 12) {
        h += 12;
      }
      let m = 0;
      if (this.min_selected == '15') { //add 30 min if selected
        m = 15;
      }
      else if (this.min_selected == '30') { //add 30 min if selected
        m = 30;
      }
      else if (this.min_selected == '45') { //add 30 min if selected
        m = 45;
      }
      this.sched_time.setHours(h,m);
      console.log("sched time:",this.sched_time);
      this.$emit('new-sched',this.sched_time,this.user_duration,this.invite_email,this.priv_bool);
    }
  }
};
</script>

<style scoped>
.newsession {
  background-color: rgba(250, 251, 251, 1);
  border-radius: 10px;
  padding: 24px 48px 30px;
  box-shadow: 0px 3px 6px 0px rgba(0, 0, 0, 0.15);
  height: 289px;
  /*display: flex;
  flex-direction: column;
  align-items: center;*/
}
.newsession-headertext {
  margin-bottom: 48px;
  display: flex;
  flex-direction: row;
  align-items: flex-start;
  justify-content: space-between;
  width: 837px;
}
.new-session {
  width: 286px;
  font-family: "Source Sans Pro";
  font-size: 18px;
  font-weight: 600;
  line-height: 27px;
  color: rgba(66, 62, 61, 1);
  text-transform: uppercase;
  letter-spacing: 1px;
}
.rooms-open-5-minutes {
  width: 545px;
  font-family: "Source Sans Pro";
  font-size: 16px;
  font-weight: 400;
  line-height: 24px;
  color: rgba(66, 62, 61, 1);
  text-align: right;
  letter-spacing: 1.6px;
}
.flex-wrapper1 {
  margin-bottom: 23px;
  display: flex;
  flex-direction: row;
  align-items: center;
}
.flex-wrapper3 {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  &:not(:last-of-type) {
    margin-right: 81px;
  }
}
.newsession-starttime {
  margin-bottom: 10px;
  display: flex;
  flex-direction: row;
  align-items: center;
}
.start-time {
  width: 109px;
  font-family: "Source Sans Pro";
  font-size: 16px;
  font-weight: 400;
  line-height: 24px;
  color: rgba(66, 62, 61, 1);
  margin-right: 24px;
  letter-spacing: 2px;
}
.schedule-starttime {
  margin-right: 19px;
}
.ampm-toggle {
  display: flex;
  flex-direction: row;
  align-items: flex-start;
}
.group-5 {
  margin-right: 7px;
  padding: 0px 1px 0px 0px;
  display: flex;
  align-items: flex-start;
  position: relative;
}
.am-highlight {
  position: relative;
}
.am1 {
  width: 38px;
  font-family: "Source Sans Pro";
  font-size: 14px;
  font-weight: 600;
  line-height: 24px;
  color: rgba(239, 235, 220, 1);
  text-align: center;
  text-transform: uppercase;
  position: absolute;
  right: 1px;
  top: 2px;
  letter-spacing: 2px;
}
.pm1 {
  width: 33px;
  font-family: "Source Sans Pro";
  font-size: 16px;
  font-weight: 400;
  line-height: 24px;
  color: rgba(51, 46, 45, 1);
  text-align: center;
  margin-top: 2px;
  opacity: 0.5;
  letter-spacing: 2px;
  cursor: pointer;
}
.newsession-duration {
  padding: 1px 0px 0px;
  display: flex;
  flex-direction: row;
  align-items: flex-start;
}
.duration {
  width: 109px;
  font-family: "Source Sans Pro";
  font-size: 16px;
  font-weight: 400;
  line-height: 24px;
  color: rgba(66, 62, 61, 1);
  margin-top: 18px;
  margin-right: 112px;
  letter-spacing: 2px;
}
.entry-totaldurationmin {
  margin-right: 24px;
  width: 80px;
}
.minutes {
  width: 76px;
  font-family: "Source Sans Pro";
  font-size: 16px;
  font-weight: 400;
  line-height: 24px;
  color: rgba(66, 62, 61, 1);
  margin-top: 18px;
  margin-right: 80px;
  letter-spacing: 2px;
}
.invite-friend {
  width: 146px;
  font-family: "Source Sans Pro";
  font-size: 16px;
  font-weight: 400;
  line-height: 24px;
  color: rgba(66, 62, 61, 1);
  margin-top: 4px;
  margin-bottom: 13px;
  letter-spacing: 2px;
}
.invite-friend-input {
  width: 355px;
}
.flex-wrapper2 {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
  width: 837px;
}
.icons-chevron-down {
  width: 24px;
  height: 24px;
}

.schedule-new-starttime {
  display: flex;
  align-items: flex-start;
  position: relative;
}
.group-6 {
  display: flex;
  flex-direction: row;
  align-items: center;
  position: relative;
}
.hour {
  background-color: rgba(250, 251, 251, 1);
  border-radius: 10px;
  padding: 2px 9px 1px 15px;
  display: flex;
  flex-direction: row;
  align-items: center;
  border: 1px solid rgba(63, 80, 42, 0.25);
  margin-right: 8px;
  cursor: pointer;
  width: 80px;
}
.hour2 {
  background-color: rgba(250, 251, 251, 1);
  border-radius: 10px;
  padding: 2px 9px 1px 15px;
  display: flex;
  flex-direction: row;
  align-items: center;
  border: 1px solid rgba(63, 80, 42, 0.25);
  cursor: pointer;
  width: 80px;
}
.num-12 {
  width: 24px;
  font-family: "Source Sans Pro";
  font-size: 18px;
  font-weight: 600;
  line-height: 27px;
  color: rgba(66, 62, 61, 1);
  text-align: center;
  text-transform: uppercase;
  margin-right: 6px;
  letter-spacing: 1px;
}
.oval {
  background-color: rgba(216, 216, 216, 1);
  border-radius: 50%;
  position: absolute;
  left: 83px;
  top: 12px;
  border: 1px solid rgba(151, 151, 151, 1);
}
.oval-copy {
  background-color: rgba(216, 216, 216, 1);
  border-radius: 50%;
  position: absolute;
  left: 83px;
  bottom: 12px;
  border: 1px solid rgba(151, 151, 151, 1);
}

.active-highlight {
  border-radius: 16px;
  padding: 23px 10px 7px 9px;
  display: flex;
  align-items: flex-start;
  background: linear-gradient(
    126deg,
    rgba(80, 88, 75, 1) 58%,
    rgba(104, 119, 94, 1) 58%,
    rgba(41, 44, 37, 1) 122%
  );
}
.underline1 {
  width: 21px;
  height: 2px;
  background-color: rgba(238, 242, 244, 1);
  border-radius: 1px;
}

.input {
  /*width: 267px;*/
  background-color: $white-empty-nofill;
  border-radius: 5px;
  padding: 14px 0px 14px 12px;
  border: 1px solid rgba(63, 80, 42, 0.25);
  font-family: "Source Sans Pro";
  font-size: 14px;
  font-weight: 400;
  line-height: 24px;
  color: rgba(66, 62, 61, 1);
  letter-spacing: 2px;
  &::placeholder {
    width: 267px;
    font-family: "Source Sans Pro";
    font-size: 14px;
    font-weight: 400;
    line-height: 24px;
    color: rgba(66, 62, 61, 1);
    opacity: 0.5;
    letter-spacing: 2px;
  }
}

.group-2 {
  display: flex;
  flex-direction: row;
  align-items: center;
}
.unselected {
  width: 14px;
  height: 14px;
  background-color: rgba(250, 251, 251, 1);
  border-radius: 3px;
  border: 1px solid rgba(63, 80, 42, 0.25);
  margin-right: 10px;
  cursor: pointer;
}
.selected-rec {
  width: 14px;
  height: 14px;
  border-radius: 3px;
  box-shadow: 0px 1px 1px 0px rgba(0, 0, 0, 0.5) inset;
  background: linear-gradient(
    216deg,
    rgba(115, 136, 84, 1) 8%,
    rgba(63, 80, 42, 1) 107%
  );
  margin-right: 10px;
  cursor: pointer;
}

.private {
  width: 64px;
  font-family: "Source Sans Pro";
  font-size: 16px;
  font-weight: 400;
  line-height: 24px;
  color: rgba(66, 62, 61, 1);
  margin-right: 16px;
  letter-spacing: 2px;
}

.icons-info {
  width: 24px;
  height: 24px;
  cursor: pointer;
}

.button-dark {
  position: absolute;
  top: 216px;
  left: 729px;

  border-radius: 19px;
  padding: 8px 38px;
  box-shadow: 0px 2px 10px 0px rgba(116, 115, 115, 0.33);
  display: flex;
  align-items: flex-start;
  cursor: pointer;
  background: linear-gradient(
    103deg,
    rgba(41, 44, 37, 1) 61%,
    rgba(104, 119, 94, 1) 125%,
    rgba(80, 88, 75, 1) 125%
  );
}
.confirm {
  width: 79px;
  font-family: "Source Sans Pro";
  font-size: 14px;
  font-weight: 600;
  line-height: 24px;
  color: rgba(239, 235, 220, 1);
  text-align: center;
  text-transform: uppercase;
  letter-spacing: 2px;
}

.toggle-ampm {
  padding: 0px 1px;
  display: flex;
  align-items: flex-start;
}
.group-6 {
  display: flex;
  flex-direction: row;
  align-items: flex-start;
}
.amreactive {
  margin-top: 2px;
  margin-right: 1px;
  padding: 0px 2px 0px 0px;
  display: flex;
  align-items: flex-start;
}
.am2 {
  width: 39px;
  font-family: "Source Sans Pro";
  font-size: 16px;
  font-weight: 400;
  line-height: 24px;
  color: rgba(51, 46, 45, 1);
  text-align: center;
  opacity: 0.5;
  letter-spacing: 2px;
  cursor: pointer;
}
.relative-wrapper1 {
  display: flex;
  align-items: flex-start;
  position: relative;
}
.selectedhighlight {
  width: 40px;
  height: 32px;
  border-radius: 16px;
  background: linear-gradient(
    126deg,
    rgba(80, 88, 75, 1) 58%,
    rgba(104, 119, 94, 1) 58%,
    rgba(41, 44, 37, 1) 122%
  );
  position: relative;
}
.underline2 {
  width: 21px;
  height: 2px;
  background-color: rgba(238, 242, 244, 1);
  border-radius: 1px;
  position: absolute;
  left: 9px;
  bottom: 8px;
}
.pm2 {
  width: 33px;
  font-family: "Source Sans Pro";
  font-size: 14px;
  font-weight: 600;
  line-height: 24px;
  color: rgba(239, 235, 220, 1);
  text-align: center;
  text-transform: uppercase;
  position: absolute;
  right: 3px;
  top: 2px;
  letter-spacing: 2px;
}

.dropdownboundarybox-hr {
  background-color: rgba(250, 251, 251, 1);
  border-radius: 10px;
  padding: 3px 7px 2px 15px;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  border: 1px solid rgba(63, 80, 42, 0.25);
  position: absolute;
  width: 80px;
  /*top: 96px;
  left: 181px;*/
}
.num-1 {
  width: 24px;
  font-family: "Source Sans Pro";
  font-size: 18px;
  font-weight: 600;
  line-height: 27px;
  color: rgba(66, 62, 61, 1);
  text-align: center;
  text-transform: uppercase;
  margin-bottom: 4px;
  margin-right: 8px;
  letter-spacing: 1px;
}
.flex-wrapper-hour {
  display: flex;
  flex-direction: row;
  align-items: center;
  width: 80px;
  cursor: pointer;
}
.num-12 {
  width: 24px;
  font-family: "Source Sans Pro";
  font-size: 18px;
  font-weight: 600;
  line-height: 27px;
  color: rgba(66, 62, 61, 1);
  text-align: center;
  text-transform: uppercase;
  margin-right: 8px;
  letter-spacing: 1px;
}

.dropdownboundarybox-min {
  background-color: rgba(250, 251, 251, 1);
  border-radius: 10px;
  padding: 3px 7px 3px 15px;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  border: 1px solid rgba(63, 80, 42, 0.25);
  position: absolute;
  width: 80px;
  left: 88px;
}
.flex-wrapper-min {
  display: flex;
  flex-direction: row;
  align-items: center;
  width: 80px;
}
.num-00 {
  width: 24px;
  font-family: "Source Sans Pro";
  font-size: 18px;
  font-weight: 600;
  line-height: 27px;
  color: rgba(66, 62, 61, 1);
  text-align: center;
  text-transform: uppercase;
  margin-right: 8px;
  letter-spacing: 1px;
  margin-bottom: 4px;
}
</style>