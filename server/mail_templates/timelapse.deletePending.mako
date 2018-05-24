<%include file="_header.mako"/>

<div style="font-size: 18px; font-weight: bold; color: #ceb239; margin-bottom: 12px;">
Your timelapse photos and generated video are set to expire soon.
</div>

<p>
As a matter of policy, we automatically remove your timelapse photos and videos from our servers
after ${days} days. Your timelapse series <b>${folder['name']}</b> is scheduled for deletion on
<b>${deletionDate}</b>.
</p>

<p>
If you wish to retain this dataset for yourself, please download the corresponding files from
<a href="${url}">this page</a> prior to that date.
</p>

<p style="margin-top: 20px">
Thanks for using our service!
</p>

<p style="color: #888">
&mdash; <i>The Kitware algorithms team</i>
</p>

<%include file="_footer.mako"/>
