<template>
<div>
    <Parent
        :week="FormsData.week"
        @newWeekNum="changeWeekNum"
        />
    <Child/>

        <button @click="AddFileds" class="btn btn-primary"> Add fields </button> <br>
        <Table v-model="FormsData.weeklyDetail"></Table>
        <button @click="Submit" class="btn btn-primary"> Submit </button>
</div>
</template>

<script>
import Parent from "./ParentForms.vue"
import Child from "./ChildForms.vue"
import Table from "./Table.vue"

export default {
    name: "Container",
    components: {
        Parent,
        Child,
        Table,
        
    },
    data() {
        return {
        FormsData:{
            fcName: "FC001",
            week: 1,
        },
        Week: 0,
        }
    },
    methods:{
        AddFileds(){
            this.FormsData.weeklyDetail.push({})
        },
        Submit(){
            const request = new Request(
            "http://localhost:8888/submitWeekData",
            {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(this.FormsData)
            }
            );
            fetch(request)
                .then(response => response.json())
                .catch((error) => console.log(error.message))
            this.FormsData.week += 1;
        },
        changeWeekNum(num, fcname) {
            this.FormsData.week = num
            this.FormsData.fcName = fcname
        },
        
    },
    
    // updated() {
    //     this.$watch("FormsData.week", () =>{
        
    //     })
    // }
}
</script>
