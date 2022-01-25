<template>
<div>
    <Parent
        @headerData="headerData"
        @details="populateDetails"
        ref="form"
    />
    <br>
    <Child
        v-model="FormsData.weeklyDetail"
        @onDelete="deleteObj"
    />
    <Table v-model="FormsData.weeklyDetail"></Table>
    <Button
        :msg="msg"
        @click="submit"
    />
    <!-- <button @click="submit" class="btn btn-primary"> Submit </button> -->
</div>
</template>

<script>
import Parent from "./ParentForms.vue"
import Child from "./ChildForms.vue"
import Table from "./Table.vue"
import Button from "./Button.vue"

export default {
    name: "Container",
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
                weeklyDetail: [{}],
            },
            msg: "",
        }
    },
    watch:{
        msg(newval){
            this.$emit("msg", newval)
        }
    },
    methods:{
        submit(){
            console.log(this.FormsData)
            const request = new Request(
            "http://www.nss-irt-t.xyz:8888/submitWeekData",
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
            this.FormsData.weeklyDetail = []
            if (details.length == 0) {
                this.FormsData.weeklyDetail.push({})
                this.msg = "Add"
                // this.changeTitle("Add")
            }
            for (let i = 0; i < details.length; i++) {
                let obj = {}
                obj.power = details[i].Power   
                obj.fromDate = details[i].FromDate
                obj.toDate = details[i].ToDate
                this.FormsData.weeklyDetail.push(obj)
                this.msg = "Update"
            }
        },
        deleteObj(index){
            this.FormsData.weeklyDetail = this.FormsData.weeklyDetail.filter((_, indx) => indx != index)
        },
        prePopTimeField(){

        }
    },
}
</script>
