import $ from 'jquery';
import { Layout } from 'girder/constants';
import events from 'girder/events';
import ItemModel from 'girder/models/ItemModel';
import ItemView from 'girder/views/body/ItemView';
import router from 'girder/router';
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
