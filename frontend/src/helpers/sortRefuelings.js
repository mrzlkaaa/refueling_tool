
export default function(a, b) {
        a  = a.toString();
        b = b.toString();
        a = parseInt(a.slice(0,3))
        b = parseInt(b.slice(0,3))
        return b - a
}