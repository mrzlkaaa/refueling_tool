<template>
    <div class='row'>
            <div class='col center-text'>
                    <table class="table">
                        <thead>
                            <TableRowHeader
                            :datas="header"
                            />
                        </thead>
                        <tbody>
                            <tr v-for="i,index in values" v-bind:key="index">
                                <th>{{i.power}}</th>
                                <td>{{TotalHours(index, Date.parse(i.toDate), Date.parse(i.fromDate))}} </td>
                                <td>{{EnergyOutput(index)}}</td>
                            </tr>
                            <TableRowHeader
                            :datas="['Sum', sumTime, sumEnOut]"
                            />
                        </tbody>
                    </table>
            </div>
        </div>
</template>

<script>
import TableRowHeader from "../TableRowHeader.vue"
export default {
    name: "Table",
    components: {
        TableRowHeader,
    },
    props: ["modelValue"],
    data(){
        return {
            sumTime: 0,
            sumEnOut: 0,
            header: ['Power, kW', 'Sum Time, h', 'Energy Output, MW×hour'],
        }
    },
    computed:{
        values: {
            get(){
                return this.modelValue
            },
            set(val){
                this.$emit("update:modelValue", val)
            }
        },
    },
    methods: {
        TotalHours(index, to, from) {
            this.values[index].totalHours = (to-from)/1000/3600
            return this.values[index].totalHours.toFixed(2)
        },
        EnergyOutput(index) {
            this.values[index].energyOutput = (this.values[index].power*this.values[index].totalHours)/1000
            return this.values[index].energyOutput.toFixed(2)
        },
        weeklyOuts(){
            let s = (e) => {
                let sum = 0
                for (var i of e){
                    sum += i
                }
                return sum.toFixed(2)
            }
            this.sumTime = s(this.values.map(obj => obj.totalHours))
            this.sumEnOut = s(this.values.map(obj => obj.energyOutput))   
        }
    },
    updated(){
        this.weeklyOuts()
    }

}
</script>
<style>
</style>