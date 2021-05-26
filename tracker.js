const express = require('express')
const app = express()
var exphbs = require('express-handlebars')

app.use('/static', express.static('public'));

app.engine('handlebars', exphbs({defaultLayout: 'main'}))
app.set('view engine', 'handlebars');

app.get('/', (req, res) => res.send('Hello World!'))

app.listen(3000, () => console.log('Hello world on port 3000!'))