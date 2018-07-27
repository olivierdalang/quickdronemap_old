<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis labelsEnabled="1" maxScale="0" simplifyDrawingHints="1" readOnly="0" minScale="1e+8" version="3.3.0-Master" simplifyLocal="1" simplifyDrawingTol="1" simplifyMaxScale="1" simplifyAlgorithm="0" hasScaleBasedVisibilityFlag="0">
  <renderer-v2 type="singleSymbol" enableorderby="0" symbollevels="0" forceraster="0">
    <symbols>
      <symbol type="marker" clip_to_extent="1" alpha="1" name="0">
        <layer pass="0" class="SimpleMarker" locked="0" enabled="1">
          <prop v="0" k="angle"/>
          <prop v="255,0,0,255" k="color"/>
          <prop v="1" k="horizontal_anchor_point"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="cross2" k="name"/>
          <prop v="0,0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="255,0,0,255" k="outline_color"/>
          <prop v="solid" k="outline_style"/>
          <prop v="0.5" k="outline_width"/>
          <prop v="3x:0,0,0,0,0,0" k="outline_width_map_unit_scale"/>
          <prop v="MM" k="outline_width_unit"/>
          <prop v="diameter" k="scale_method"/>
          <prop v="6" k="size"/>
          <prop v="3x:0,0,0,0,0,0" k="size_map_unit_scale"/>
          <prop v="MM" k="size_unit"/>
          <prop v="1" k="vertical_anchor_point"/>
          <data_defined_properties>
            <Option type="Map">
              <Option type="QString" value="" name="name"/>
              <Option name="properties"/>
              <Option type="QString" value="collection" name="type"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
    </symbols>
    <rotation/>
    <sizescale/>
  </renderer-v2>
  <labeling type="simple">
    <settings>
      <text-style fontSize="8" fontCapitals="0" fontSizeUnit="Point" fontStrikeout="0" useSubstitutions="0" fontWeight="50" namedStyle="Regular" fontUnderline="0" isExpression="1" fontWordSpacing="0" fontItalic="0" fontFamily="Consolas" blendMode="0" textColor="0,0,0,255" previewBkgrdColor="#ffffff" fontSizeMapUnitScale="3x:0,0,0,0,0,0" fieldName=" regexp_substr(&quot;path&quot;,'.*\\\\(.+)')" multilineHeight="1" textOpacity="1" fontLetterSpacing="0">
        <text-buffer bufferBlendMode="0" bufferOpacity="0.8" bufferSizeMapUnitScale="3x:0,0,0,0,0,0" bufferSize="1" bufferSizeUnits="MM" bufferNoFill="1" bufferDraw="1" bufferColor="255,255,255,255" bufferJoinStyle="128"/>
        <background shapeOffsetX="0" shapeJoinStyle="64" shapeOffsetMapUnitScale="3x:0,0,0,0,0,0" shapeRadiiY="0" shapeSizeType="0" shapeBlendMode="0" shapeBorderWidthMapUnitScale="3x:0,0,0,0,0,0" shapeSizeX="0" shapeBorderWidth="0" shapeRotationType="0" shapeRotation="0" shapeRadiiX="0" shapeSVGFile="" shapeRadiiUnit="MM" shapeBorderColor="128,128,128,255" shapeOpacity="1" shapeType="0" shapeDraw="0" shapeRadiiMapUnitScale="3x:0,0,0,0,0,0" shapeSizeUnit="MM" shapeOffsetY="0" shapeSizeY="0" shapeSizeMapUnitScale="3x:0,0,0,0,0,0" shapeOffsetUnit="MM" shapeFillColor="255,255,255,255" shapeBorderWidthUnit="MM"/>
        <shadow shadowUnder="0" shadowRadiusMapUnitScale="3x:0,0,0,0,0,0" shadowOffsetGlobal="1" shadowScale="100" shadowOffsetAngle="135" shadowOffsetUnit="MM" shadowDraw="0" shadowBlendMode="6" shadowRadiusUnit="MM" shadowRadiusAlphaOnly="0" shadowColor="0,0,0,255" shadowOffsetMapUnitScale="3x:0,0,0,0,0,0" shadowOpacity="0.7" shadowOffsetDist="1" shadowRadius="1.5"/>
        <substitutions/>
      </text-style>
      <text-format wrapChar="" addDirectionSymbol="0" multilineAlign="3" formatNumbers="0" decimals="3" plussign="0" rightDirectionSymbol=">" placeDirectionSymbol="0" leftDirectionSymbol="&lt;" reverseDirectionSymbol="0"/>
      <placement offsetUnits="MM" centroidWhole="0" distMapUnitScale="3x:0,0,0,0,0,0" maxCurvedCharAngleIn="25" rotationAngle="0" predefinedPositionOrder="TR,TL,BR,BL,R,L,TSR,BSR" labelOffsetMapUnitScale="3x:0,0,0,0,0,0" repeatDistanceMapUnitScale="3x:0,0,0,0,0,0" placement="1" centroidInside="0" xOffset="2" preserveRotation="1" dist="0" offsetType="0" maxCurvedCharAngleOut="-25" distUnits="MM" priority="5" repeatDistance="0" fitInPolygonOnly="0" placementFlags="10" yOffset="0" quadOffset="5" repeatDistanceUnits="MM"/>
      <rendering scaleVisibility="0" obstacleType="0" fontLimitPixelSize="0" displayAll="1" zIndex="0" scaleMax="0" limitNumLabels="0" labelPerPart="0" scaleMin="0" obstacleFactor="1" minFeatureSize="0" fontMaxPixelSize="10000" maxNumLabels="2000" fontMinPixelSize="3" obstacle="1" upsidedownLabels="0" drawLabels="1" mergeLines="0"/>
      <dd_properties>
        <Option type="Map">
          <Option type="QString" value="" name="name"/>
          <Option name="properties"/>
          <Option type="QString" value="collection" name="type"/>
        </Option>
      </dd_properties>
    </settings>
  </labeling>
  <customproperties/>
  <blendMode>0</blendMode>
  <featureBlendMode>0</featureBlendMode>
  <layerOpacity>1</layerOpacity>
  <fieldConfiguration>
    <field name="drone_map">
      <editWidget type="">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="path">
      <editWidget type="">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="prev_image">
      <editWidget type="">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="next_image">
      <editWidget type="">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="neighbours_images">
      <editWidget type="">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="width">
      <editWidget type="">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="height">
      <editWidget type="">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="lat">
      <editWidget type="">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="lon">
      <editWidget type="">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="altitude">
      <editWidget type="">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="direction">
      <editWidget type="">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="focal">
      <editWidget type="">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="timestamp">
      <editWidget type="">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="point">
      <editWidget type="">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="d_lat">
      <editWidget type="">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="d_lon">
      <editWidget type="">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="d_altitude">
      <editWidget type="">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="d_direction">
      <editWidget type="">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="d_focal">
      <editWidget type="">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="a">
      <editWidget type="">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="b">
      <editWidget type="">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="c">
      <editWidget type="">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="d">
      <editWidget type="">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="e">
      <editWidget type="">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="f">
      <editWidget type="">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="bounding_box">
      <editWidget type="">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
  </fieldConfiguration>
  <aliases>
    <alias field="drone_map" index="0" name=""/>
    <alias field="path" index="1" name=""/>
    <alias field="prev_image" index="2" name=""/>
    <alias field="next_image" index="3" name=""/>
    <alias field="neighbours_images" index="4" name=""/>
    <alias field="width" index="5" name=""/>
    <alias field="height" index="6" name=""/>
    <alias field="lat" index="7" name=""/>
    <alias field="lon" index="8" name=""/>
    <alias field="altitude" index="9" name=""/>
    <alias field="direction" index="10" name=""/>
    <alias field="focal" index="11" name=""/>
    <alias field="timestamp" index="12" name=""/>
    <alias field="point" index="13" name=""/>
    <alias field="d_lat" index="14" name=""/>
    <alias field="d_lon" index="15" name=""/>
    <alias field="d_altitude" index="16" name=""/>
    <alias field="d_direction" index="17" name=""/>
    <alias field="d_focal" index="18" name=""/>
    <alias field="a" index="19" name=""/>
    <alias field="b" index="20" name=""/>
    <alias field="c" index="21" name=""/>
    <alias field="d" index="22" name=""/>
    <alias field="e" index="23" name=""/>
    <alias field="f" index="24" name=""/>
    <alias field="bounding_box" index="25" name=""/>
  </aliases>
  <excludeAttributesWMS/>
  <excludeAttributesWFS/>
  <defaults>
    <default applyOnUpdate="0" field="drone_map" expression=""/>
    <default applyOnUpdate="0" field="path" expression=""/>
    <default applyOnUpdate="0" field="prev_image" expression=""/>
    <default applyOnUpdate="0" field="next_image" expression=""/>
    <default applyOnUpdate="0" field="neighbours_images" expression=""/>
    <default applyOnUpdate="0" field="width" expression=""/>
    <default applyOnUpdate="0" field="height" expression=""/>
    <default applyOnUpdate="0" field="lat" expression=""/>
    <default applyOnUpdate="0" field="lon" expression=""/>
    <default applyOnUpdate="0" field="altitude" expression=""/>
    <default applyOnUpdate="0" field="direction" expression=""/>
    <default applyOnUpdate="0" field="focal" expression=""/>
    <default applyOnUpdate="0" field="timestamp" expression=""/>
    <default applyOnUpdate="0" field="point" expression=""/>
    <default applyOnUpdate="0" field="d_lat" expression=""/>
    <default applyOnUpdate="0" field="d_lon" expression=""/>
    <default applyOnUpdate="0" field="d_altitude" expression=""/>
    <default applyOnUpdate="0" field="d_direction" expression=""/>
    <default applyOnUpdate="0" field="d_focal" expression=""/>
    <default applyOnUpdate="0" field="a" expression=""/>
    <default applyOnUpdate="0" field="b" expression=""/>
    <default applyOnUpdate="0" field="c" expression=""/>
    <default applyOnUpdate="0" field="d" expression=""/>
    <default applyOnUpdate="0" field="e" expression=""/>
    <default applyOnUpdate="0" field="f" expression=""/>
    <default applyOnUpdate="0" field="bounding_box" expression=""/>
  </defaults>
  <constraints>
    <constraint exp_strength="0" unique_strength="0" notnull_strength="0" field="drone_map" constraints="0"/>
    <constraint exp_strength="0" unique_strength="0" notnull_strength="0" field="path" constraints="0"/>
    <constraint exp_strength="0" unique_strength="0" notnull_strength="0" field="prev_image" constraints="0"/>
    <constraint exp_strength="0" unique_strength="0" notnull_strength="0" field="next_image" constraints="0"/>
    <constraint exp_strength="0" unique_strength="0" notnull_strength="0" field="neighbours_images" constraints="0"/>
    <constraint exp_strength="0" unique_strength="0" notnull_strength="0" field="width" constraints="0"/>
    <constraint exp_strength="0" unique_strength="0" notnull_strength="0" field="height" constraints="0"/>
    <constraint exp_strength="0" unique_strength="0" notnull_strength="0" field="lat" constraints="0"/>
    <constraint exp_strength="0" unique_strength="0" notnull_strength="0" field="lon" constraints="0"/>
    <constraint exp_strength="0" unique_strength="0" notnull_strength="0" field="altitude" constraints="0"/>
    <constraint exp_strength="0" unique_strength="0" notnull_strength="0" field="direction" constraints="0"/>
    <constraint exp_strength="0" unique_strength="0" notnull_strength="0" field="focal" constraints="0"/>
    <constraint exp_strength="0" unique_strength="0" notnull_strength="0" field="timestamp" constraints="0"/>
    <constraint exp_strength="0" unique_strength="0" notnull_strength="0" field="point" constraints="0"/>
    <constraint exp_strength="0" unique_strength="0" notnull_strength="0" field="d_lat" constraints="0"/>
    <constraint exp_strength="0" unique_strength="0" notnull_strength="0" field="d_lon" constraints="0"/>
    <constraint exp_strength="0" unique_strength="0" notnull_strength="0" field="d_altitude" constraints="0"/>
    <constraint exp_strength="0" unique_strength="0" notnull_strength="0" field="d_direction" constraints="0"/>
    <constraint exp_strength="0" unique_strength="0" notnull_strength="0" field="d_focal" constraints="0"/>
    <constraint exp_strength="0" unique_strength="0" notnull_strength="0" field="a" constraints="0"/>
    <constraint exp_strength="0" unique_strength="0" notnull_strength="0" field="b" constraints="0"/>
    <constraint exp_strength="0" unique_strength="0" notnull_strength="0" field="c" constraints="0"/>
    <constraint exp_strength="0" unique_strength="0" notnull_strength="0" field="d" constraints="0"/>
    <constraint exp_strength="0" unique_strength="0" notnull_strength="0" field="e" constraints="0"/>
    <constraint exp_strength="0" unique_strength="0" notnull_strength="0" field="f" constraints="0"/>
    <constraint exp_strength="0" unique_strength="0" notnull_strength="0" field="bounding_box" constraints="0"/>
  </constraints>
  <constraintExpressions>
    <constraint field="drone_map" desc="" exp=""/>
    <constraint field="path" desc="" exp=""/>
    <constraint field="prev_image" desc="" exp=""/>
    <constraint field="next_image" desc="" exp=""/>
    <constraint field="neighbours_images" desc="" exp=""/>
    <constraint field="width" desc="" exp=""/>
    <constraint field="height" desc="" exp=""/>
    <constraint field="lat" desc="" exp=""/>
    <constraint field="lon" desc="" exp=""/>
    <constraint field="altitude" desc="" exp=""/>
    <constraint field="direction" desc="" exp=""/>
    <constraint field="focal" desc="" exp=""/>
    <constraint field="timestamp" desc="" exp=""/>
    <constraint field="point" desc="" exp=""/>
    <constraint field="d_lat" desc="" exp=""/>
    <constraint field="d_lon" desc="" exp=""/>
    <constraint field="d_altitude" desc="" exp=""/>
    <constraint field="d_direction" desc="" exp=""/>
    <constraint field="d_focal" desc="" exp=""/>
    <constraint field="a" desc="" exp=""/>
    <constraint field="b" desc="" exp=""/>
    <constraint field="c" desc="" exp=""/>
    <constraint field="d" desc="" exp=""/>
    <constraint field="e" desc="" exp=""/>
    <constraint field="f" desc="" exp=""/>
    <constraint field="bounding_box" desc="" exp=""/>
  </constraintExpressions>
  <attributeactions>
    <defaultAction value="{00000000-0000-0000-0000-000000000000}" key="Canvas"/>
  </attributeactions>
  <attributetableconfig sortExpression="" sortOrder="0" actionWidgetStyle="dropDown">
    <columns>
      <column type="field" width="359" name="drone_map" hidden="0"/>
      <column type="field" width="470" name="path" hidden="0"/>
      <column type="field" width="270" name="prev_image" hidden="0"/>
      <column type="field" width="243" name="next_image" hidden="0"/>
      <column type="field" width="-1" name="neighbours_images" hidden="0"/>
      <column type="field" width="-1" name="width" hidden="0"/>
      <column type="field" width="-1" name="height" hidden="0"/>
      <column type="field" width="-1" name="lat" hidden="0"/>
      <column type="field" width="-1" name="lon" hidden="0"/>
      <column type="field" width="-1" name="altitude" hidden="0"/>
      <column type="field" width="-1" name="direction" hidden="0"/>
      <column type="field" width="-1" name="focal" hidden="0"/>
      <column type="field" width="-1" name="timestamp" hidden="0"/>
      <column type="field" width="-1" name="point" hidden="0"/>
      <column type="field" width="-1" name="d_lat" hidden="0"/>
      <column type="field" width="-1" name="d_lon" hidden="0"/>
      <column type="field" width="-1" name="d_altitude" hidden="0"/>
      <column type="field" width="-1" name="d_direction" hidden="0"/>
      <column type="field" width="-1" name="d_focal" hidden="0"/>
      <column type="field" width="-1" name="a" hidden="0"/>
      <column type="field" width="-1" name="b" hidden="0"/>
      <column type="field" width="-1" name="c" hidden="0"/>
      <column type="field" width="-1" name="d" hidden="0"/>
      <column type="field" width="-1" name="e" hidden="0"/>
      <column type="field" width="-1" name="f" hidden="0"/>
      <column type="field" width="-1" name="bounding_box" hidden="0"/>
      <column type="actions" width="-1" hidden="1"/>
    </columns>
  </attributetableconfig>
  <editform></editform>
  <editforminit/>
  <editforminitcodesource>0</editforminitcodesource>
  <editforminitfilepath></editforminitfilepath>
  <editforminitcode><![CDATA[]]></editforminitcode>
  <featformsuppress>0</featformsuppress>
  <editorlayout>generatedlayout</editorlayout>
  <editable/>
  <labelOnTop/>
  <widgets/>
  <conditionalstyles>
    <rowstyles/>
    <fieldstyles/>
  </conditionalstyles>
  <expressionfields/>
  <previewExpression>"width"</previewExpression>
  <mapTip></mapTip>
  <layerGeometryType>0</layerGeometryType>
</qgis>
