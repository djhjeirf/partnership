/**
 * Created by User on 29.09.2016.
 */

function add_owner(){
    var text = '<tr><td valign="top"><div>Владелец</div><select name="owners"><option></option>' +
        '{% for o in o_list %}<option>{{ o }}</option>{% endfor %}</select></td><td colspan="2"><div>Документ</div>' +
        '<textarea rows="5" name="document"></textarea></td></tr>';
    $('.plot-table-add').append(text);
}