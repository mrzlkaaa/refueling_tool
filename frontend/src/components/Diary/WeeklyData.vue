<template>
    <div class="card-body">
        <Parent
            @headerData="headerData"
            @details="populateDetails"
            ref="form"
        />
        <br>
        <Child
            v-model="FormsData"
            @onDelete="deleteObj"
        />
        <Table v-model="FormsData.weeklyDetail"></Table>
            <div v-if="msg.length>0">
            <Button
            :msg="msg"
            class="btn btn-primary"
            @click="submit"
            />
            </div>
    </div>
</template>

 <script>
import Button from "./Button.vue"
import Parent from "./ParentForms.vue"
import Child from "./ChildForms.vue"
import Table from "./TableWeeklyData.vue"
 export default {
    name: "WeeklyData",
    components: {
        Parent,
        Child,
        Table,
        Button,
    },
    data() {
        return {
            FormsData:{
                fcName: "",
                week: 0,
                rodsPosition:{
                    AR:0,
                    KS1: 0,
                    KS2: 0,
                    KS3: 0,
                    Temp: 0.0,
                },
                weeklyDetail: [{}],
            },
            msg: "Submit",
        }
    },
    watch:{
        msg(newval){
            this.$emit("msg", newval)
            console.log(this.FormsData)
        }
    },
    methods:{
        submit(){
            console.log(this.FormsData)
            const request = new Request(
            `${this.diaryDepHost}/submitWeekData`,
            {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(this.FormsData)
            }
            );
            fetch(request)
                .then(response => response.json())
                .catch((error) => console.log(error.message))
                //* call api to see updates on weeks
                setTimeout(this.$refs.form.getWeeksNum, 500, this.$refs.form.fcName)
            
        },
        headerData(num, fcname) {
            this.FormsData.week = num
            this.FormsData.fcName = fcname
        },
        populateDetails(details) {
            console.log(details)
            this.FormsData.weeklyDetail = []
            if (details.DetailWeek == null) {
                this.FormsData.weeklyDetail.push({})
                this.msg = "Add Data"
                // this.changeTitle("Add")
            }
            for (let i = 0; i < details.DetailWeek.length; i++) {
                let obj = {}
                obj.power = details.DetailWeek[i].Power   
                obj.fromDate = details.DetailWeek[i].FromDate
                obj.toDate = details.DetailWeek[i].ToDate
                this.FormsData.weeklyDetail.push(obj)
                this.msg = "Update Data"
            }
            this.FormsData.rodsPosition = details.RodsPosition
        },
        deleteObj(index){
            this.FormsData.weeklyDetail = this.FormsData.weeklyDetail.filter((_, indx) => indx != index)
        },
        prePopTimeField(){

        }
    },
 }
 </script>
