import $ from 'jquery';
import ItemListWidget from 'girder/views/widgets/ItemListWidget';
import ItemView from 'girder/views/body/ItemView';
import { wrap } from 'girder/utilities/PluginUtils'

import itemActionsExt from './itemActionsExt.pug';

// Add menu item to item actions menu
wrap(ItemView, 'render', function (render) {
    this.once('g:rendered', function () {
        $(itemActionsExt({
            item: this.model
        })).prependTo(this.$('.g-item-actions-menu'));
    }, this);

    return render.call(this);
});

wrap(ItemListWidget, 'render', function (render) {
    render.call(this);
    this.$('.g-item-list-link').each((k, v) => {
        const id = this.collection.get($(v).attr('g-item-cid')).id;
        $(v).parent().find('.g-view-inline').attr({
            href: `/#/glance/${id}`,
            title: 'Open in ParaView Glance'
        });
    });
    return this;
});
