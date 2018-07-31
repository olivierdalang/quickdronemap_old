<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis maxScale="0" labelsEnabled="1" simplifyAlgorithm="0" simplifyLocal="1" simplifyMaxScale="1" hasScaleBasedVisibilityFlag="0" minScale="1e+8" version="3.3.0-Master" readOnly="0" simplifyDrawingHints="0" simplifyDrawingTol="1">
  <renderer-v2 symbollevels="0" type="singleSymbol" enableorderby="0" forceraster="0">
    <symbols>
      <symbol alpha="1" type="marker" clip_to_extent="1" name="0">
        <layer enabled="1" pass="0" class="GeometryGenerator" locked="0">
          <prop v="Line" k="SymbolType"/>
          <prop v="make_line(&#xd;&#xa;    $geometry,&#xd;&#xa; transform(   geom_from_wkt (regexp_substr  ( point,'&lt;QgsPointXY:(.+)>')), 'EPSG:32628', 'EPSG:4326')&#xd;&#xa;)&#xd;&#xa;" k="geometryModifier"/>
          <data_defined_properties>
            <Option type="Map">
              <Option type="QString" value="" name="name"/>
              <Option name="properties"/>
              <Option type="QString" value="collection" name="type"/>
            </Option>
          </data_defined_properties>
          <symbol alpha="1" type="line" clip_to_extent="1" name="@0@0">
            <layer enabled="1" pass="0" class="ArrowLine" locked="0">
              <prop v="1" k="arrow_start_width"/>
              <prop v="MM" k="arrow_start_width_unit"/>
              <prop v="3x:0,0,0,0,0,0" k="arrow_start_width_unit_scale"/>
              <prop v="0" k="arrow_type"/>
              <prop v="0.5" k="arrow_width"/>
              <prop v="MM" k="arrow_width_unit"/>
              <prop v="3x:0,0,0,0,0,0" k="arrow_width_unit_scale"/>
              <prop v="1.5" k="head_length"/>
              <prop v="MM" k="head_length_unit"/>
              <prop v="3x:0,0,0,0,0,0" k="head_length_unit_scale"/>
              <prop v="1.5" k="head_thickness"/>
              <prop v="MM" k="head_thickness_unit"/>
              <prop v="3x:0,0,0,0,0,0" k="head_thickness_unit_scale"/>
              <prop v="0" k="head_type"/>
              <prop v="1" k="is_curved"/>
              <prop v="1" k="is_repeated"/>
              <prop v="0" k="offset"/>
              <prop v="MM" k="offset_unit"/>
              <prop v="3x:0,0,0,0,0,0" k="offset_unit_scale"/>
              <data_defined_properties>
                <Option type="Map">
                  <Option type="QString" value="" name="name"/>
                  <Option name="properties"/>
                  <Option type="QString" value="collection" name="type"/>
                </Option>
              </data_defined_properties>
              <symbol alpha="1" type="fill" clip_to_extent="1" name="@@0@0@0">
                <layer enabled="1" pass="0" class="SimpleFill" locked="0">
                  <prop v="3x:0,0,0,0,0,0" k="border_width_map_unit_scale"/>
                  <prop v="0,0,255,255" k="color"/>
                  <prop v="bevel" k="joinstyle"/>
                  <prop v="0,0" k="offset"/>
                  <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
                  <prop v="MM" k="offset_unit"/>
                  <prop v="35,35,35,255" k="outline_color"/>
                  <prop v="no" k="outline_style"/>
                  <prop v="0.26" k="outline_width"/>
                  <prop v="MM" k="outline_width_unit"/>
                  <prop v="solid" k="style"/>
                  <data_defined_properties>
                    <Option type="Map">
                      <Option type="QString" value="" name="name"/>
                      <Option name="properties"/>
                      <Option type="QString" value="collection" name="type"/>
                    </Option>
                  </data_defined_properties>
                </layer>
              </symbol>
            </layer>
          </symbol>
        </layer>
        <layer enabled="1" pass="0" class="SimpleMarker" locked="0">
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
      <text-style fontSizeMapUnitScale="3x:0,0,0,0,0,0" fontWeight="50" fontSizeUnit="Point" textColor="0,0,0,255" fontUnderline="0" useSubstitutions="0" textOpacity="1" fontItalic="0" previewBkgrdColor="#ffffff" fontCapitals="0" fieldName=" regexp_substr(&quot;path&quot;,'.*\\\\(.+)')" isExpression="1" namedStyle="Regular" fontStrikeout="0" fontSize="8" fontLetterSpacing="0" fontWordSpacing="0" fontFamily="Consolas" blendMode="0" multilineHeight="1">
        <text-buffer bufferSizeUnits="MM" bufferBlendMode="0" bufferOpacity="0.8" bufferDraw="1" bufferSize="1" bufferSizeMapUnitScale="3x:0,0,0,0,0,0" bufferJoinStyle="128" bufferColor="255,255,255,255" bufferNoFill="1"/>
        <background shapeOffsetUnit="MM" shapeBorderWidth="0" shapeOffsetY="0" shapeJoinStyle="64" shapeRadiiMapUnitScale="3x:0,0,0,0,0,0" shapeBorderColor="128,128,128,255" shapeSVGFile="" shapeRotation="0" shapeSizeUnit="MM" shapeSizeY="0" shapeSizeType="0" shapeDraw="0" shapeFillColor="255,255,255,255" shapeRadiiY="0" shapeBorderWidthMapUnitScale="3x:0,0,0,0,0,0" shapeBlendMode="0" shapeType="0" shapeSizeX="0" shapeRotationType="0" shapeRadiiX="0" shapeBorderWidthUnit="MM" shapeRadiiUnit="MM" shapeOffsetX="0" shapeOffsetMapUnitScale="3x:0,0,0,0,0,0" shapeSizeMapUnitScale="3x:0,0,0,0,0,0" shapeOpacity="1"/>
        <shadow shadowDraw="0" shadowRadiusUnit="MM" shadowOpacity="0.7" shadowScale="100" shadowBlendMode="6" shadowOffsetGlobal="1" shadowOffsetMapUnitScale="3x:0,0,0,0,0,0" shadowUnder="0" shadowOffsetAngle="135" shadowRadius="1.5" shadowOffsetUnit="MM" shadowRadiusMapUnitScale="3x:0,0,0,0,0,0" shadowColor="0,0,0,255" shadowOffsetDist="1" shadowRadiusAlphaOnly="0"/>
        <substitutions/>
      </text-style>
      <text-format addDirectionSymbol="0" wrapChar="" formatNumbers="0" decimals="3" leftDirectionSymbol="&lt;" multilineAlign="3" placeDirectionSymbol="0" reverseDirectionSymbol="0" rightDirectionSymbol=">" plussign="0"/>
      <placement distMapUnitScale="3x:0,0,0,0,0,0" dist="0" xOffset="2" distUnits="MM" rotationAngle="0" offsetUnits="MM" quadOffset="5" preserveRotation="1" centroidWhole="0" offsetType="0" placementFlags="10" centroidInside="0" maxCurvedCharAngleIn="25" repeatDistance="0" maxCurvedCharAngleOut="-25" labelOffsetMapUnitScale="3x:0,0,0,0,0,0" fitInPolygonOnly="0" predefinedPositionOrder="TR,TL,BR,BL,R,L,TSR,BSR" repeatDistanceUnits="MM" yOffset="0" placement="1" repeatDistanceMapUnitScale="3x:0,0,0,0,0,0" priority="5"/>
      <rendering fontMinPixelSize="3" displayAll="1" zIndex="0" scaleVisibility="0" obstacleType="0" maxNumLabels="2000" limitNumLabels="0" mergeLines="0" drawLabels="1" scaleMin="0" upsidedownLabels="0" fontMaxPixelSize="10000" obstacle="1" minFeatureSize="0" obstacleFactor="1" scaleMax="0" labelPerPart="0" fontLimitPixelSize="0"/>
      <dd_properties>
        <Option type="Map">
          <Option type="QString" value="" name="name"/>
          <Option name="properties"/>
          <Option type="QString" value="collection" name="type"/>
        </Option>
      </dd_properties>
    </settings>
  </labeling>
  <customproperties>
    <property value="0" key="embeddedWidgets/count"/>
    <property key="variableNames"/>
    <property key="variableValues"/>
  </customproperties>
  <blendMode>0</blendMode>
  <featureBlendMode>0</featureBlendMode>
  <layerOpacity>1</layerOpacity>
  <SingleCategoryDiagramRenderer attributeLegend="1" diagramType="Histogram">
    <DiagramCategory diagramOrientation="Up" sizeScale="3x:0,0,0,0,0,0" minScaleDenominator="0" backgroundAlpha="255" sizeType="MM" lineSizeScale="3x:0,0,0,0,0,0" width="15" enabled="0" lineSizeType="MM" maxScaleDenominator="1e+8" height="15" backgroundColor="#ffffff" opacity="1" penColor="#000000" penAlpha="255" penWidth="0" scaleDependency="Area" barWidth="5" labelPlacementMethod="XHeight" scaleBasedVisibility="0" minimumSize="0" rotationOffset="270">
      <fontProperties style="" description="MS Shell Dlg 2,8.25,-1,5,50,0,0,0,0,0"/>
    </DiagramCategory>
  </SingleCategoryDiagramRenderer>
  <DiagramLayerSettings zIndex="0" placement="0" obstacle="0" showAll="1" linePlacementFlags="18" dist="0" priority="0">
    <properties>
      <Option type="Map">
        <Option type="QString" value="" name="name"/>
        <Option name="properties"/>
        <Option type="QString" value="collection" name="type"/>
      </Option>
    </properties>
  </DiagramLayerSettings>
  <fieldConfiguration>
    <field name="drone_map">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="id">
      <editWidget type="Range">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="path">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="width">
      <editWidget type="Range">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="height">
      <editWidget type="Range">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="focal">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="timestamp">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="lat">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="lon">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="direction">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="altitude">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="pixel_size">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="prev_image">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="next_image">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="edges">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="point">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="angle">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="scale">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="a">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="b">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="c">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="d">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="e">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="f">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="target_angle">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="target_scale">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="target_point">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="bounding_box">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
  </fieldConfiguration>
  <aliases>
    <alias index="0" field="drone_map" name=""/>
    <alias index="1" field="id" name=""/>
    <alias index="2" field="path" name=""/>
    <alias index="3" field="width" name=""/>
    <alias index="4" field="height" name=""/>
    <alias index="5" field="focal" name=""/>
    <alias index="6" field="timestamp" name=""/>
    <alias index="7" field="lat" name=""/>
    <alias index="8" field="lon" name=""/>
    <alias index="9" field="direction" name=""/>
    <alias index="10" field="altitude" name=""/>
    <alias index="11" field="pixel_size" name=""/>
    <alias index="12" field="prev_image" name=""/>
    <alias index="13" field="next_image" name=""/>
    <alias index="14" field="edges" name=""/>
    <alias index="15" field="point" name=""/>
    <alias index="16" field="angle" name=""/>
    <alias index="17" field="scale" name=""/>
    <alias index="18" field="a" name=""/>
    <alias index="19" field="b" name=""/>
    <alias index="20" field="c" name=""/>
    <alias index="21" field="d" name=""/>
    <alias index="22" field="e" name=""/>
    <alias index="23" field="f" name=""/>
    <alias index="24" field="target_angle" name=""/>
    <alias index="25" field="target_scale" name=""/>
    <alias index="26" field="target_point" name=""/>
    <alias index="27" field="bounding_box" name=""/>
  </aliases>
  <excludeAttributesWMS/>
  <excludeAttributesWFS/>
  <defaults>
    <default applyOnUpdate="0" expression="" field="drone_map"/>
    <default applyOnUpdate="0" expression="" field="id"/>
    <default applyOnUpdate="0" expression="" field="path"/>
    <default applyOnUpdate="0" expression="" field="width"/>
    <default applyOnUpdate="0" expression="" field="height"/>
    <default applyOnUpdate="0" expression="" field="focal"/>
    <default applyOnUpdate="0" expression="" field="timestamp"/>
    <default applyOnUpdate="0" expression="" field="lat"/>
    <default applyOnUpdate="0" expression="" field="lon"/>
    <default applyOnUpdate="0" expression="" field="direction"/>
    <default applyOnUpdate="0" expression="" field="altitude"/>
    <default applyOnUpdate="0" expression="" field="pixel_size"/>
    <default applyOnUpdate="0" expression="" field="prev_image"/>
    <default applyOnUpdate="0" expression="" field="next_image"/>
    <default applyOnUpdate="0" expression="" field="edges"/>
    <default applyOnUpdate="0" expression="" field="point"/>
    <default applyOnUpdate="0" expression="" field="angle"/>
    <default applyOnUpdate="0" expression="" field="scale"/>
    <default applyOnUpdate="0" expression="" field="a"/>
    <default applyOnUpdate="0" expression="" field="b"/>
    <default applyOnUpdate="0" expression="" field="c"/>
    <default applyOnUpdate="0" expression="" field="d"/>
    <default applyOnUpdate="0" expression="" field="e"/>
    <default applyOnUpdate="0" expression="" field="f"/>
    <default applyOnUpdate="0" expression="" field="target_angle"/>
    <default applyOnUpdate="0" expression="" field="target_scale"/>
    <default applyOnUpdate="0" expression="" field="target_point"/>
    <default applyOnUpdate="0" expression="" field="bounding_box"/>
  </defaults>
  <constraints>
    <constraint exp_strength="0" notnull_strength="0" constraints="0" field="drone_map" unique_strength="0"/>
    <constraint exp_strength="0" notnull_strength="0" constraints="0" field="id" unique_strength="0"/>
    <constraint exp_strength="0" notnull_strength="0" constraints="0" field="path" unique_strength="0"/>
    <constraint exp_strength="0" notnull_strength="0" constraints="0" field="width" unique_strength="0"/>
    <constraint exp_strength="0" notnull_strength="0" constraints="0" field="height" unique_strength="0"/>
    <constraint exp_strength="0" notnull_strength="0" constraints="0" field="focal" unique_strength="0"/>
    <constraint exp_strength="0" notnull_strength="0" constraints="0" field="timestamp" unique_strength="0"/>
    <constraint exp_strength="0" notnull_strength="0" constraints="0" field="lat" unique_strength="0"/>
    <constraint exp_strength="0" notnull_strength="0" constraints="0" field="lon" unique_strength="0"/>
    <constraint exp_strength="0" notnull_strength="0" constraints="0" field="direction" unique_strength="0"/>
    <constraint exp_strength="0" notnull_strength="0" constraints="0" field="altitude" unique_strength="0"/>
    <constraint exp_strength="0" notnull_strength="0" constraints="0" field="pixel_size" unique_strength="0"/>
    <constraint exp_strength="0" notnull_strength="0" constraints="0" field="prev_image" unique_strength="0"/>
    <constraint exp_strength="0" notnull_strength="0" constraints="0" field="next_image" unique_strength="0"/>
    <constraint exp_strength="0" notnull_strength="0" constraints="0" field="edges" unique_strength="0"/>
    <constraint exp_strength="0" notnull_strength="0" constraints="0" field="point" unique_strength="0"/>
    <constraint exp_strength="0" notnull_strength="0" constraints="0" field="angle" unique_strength="0"/>
    <constraint exp_strength="0" notnull_strength="0" constraints="0" field="scale" unique_strength="0"/>
    <constraint exp_strength="0" notnull_strength="0" constraints="0" field="a" unique_strength="0"/>
    <constraint exp_strength="0" notnull_strength="0" constraints="0" field="b" unique_strength="0"/>
    <constraint exp_strength="0" notnull_strength="0" constraints="0" field="c" unique_strength="0"/>
    <constraint exp_strength="0" notnull_strength="0" constraints="0" field="d" unique_strength="0"/>
    <constraint exp_strength="0" notnull_strength="0" constraints="0" field="e" unique_strength="0"/>
    <constraint exp_strength="0" notnull_strength="0" constraints="0" field="f" unique_strength="0"/>
    <constraint exp_strength="0" notnull_strength="0" constraints="0" field="target_angle" unique_strength="0"/>
    <constraint exp_strength="0" notnull_strength="0" constraints="0" field="target_scale" unique_strength="0"/>
    <constraint exp_strength="0" notnull_strength="0" constraints="0" field="target_point" unique_strength="0"/>
    <constraint exp_strength="0" notnull_strength="0" constraints="0" field="bounding_box" unique_strength="0"/>
  </constraints>
  <constraintExpressions>
    <constraint desc="" exp="" field="drone_map"/>
    <constraint desc="" exp="" field="id"/>
    <constraint desc="" exp="" field="path"/>
    <constraint desc="" exp="" field="width"/>
    <constraint desc="" exp="" field="height"/>
    <constraint desc="" exp="" field="focal"/>
    <constraint desc="" exp="" field="timestamp"/>
    <constraint desc="" exp="" field="lat"/>
    <constraint desc="" exp="" field="lon"/>
    <constraint desc="" exp="" field="direction"/>
    <constraint desc="" exp="" field="altitude"/>
    <constraint desc="" exp="" field="pixel_size"/>
    <constraint desc="" exp="" field="prev_image"/>
    <constraint desc="" exp="" field="next_image"/>
    <constraint desc="" exp="" field="edges"/>
    <constraint desc="" exp="" field="point"/>
    <constraint desc="" exp="" field="angle"/>
    <constraint desc="" exp="" field="scale"/>
    <constraint desc="" exp="" field="a"/>
    <constraint desc="" exp="" field="b"/>
    <constraint desc="" exp="" field="c"/>
    <constraint desc="" exp="" field="d"/>
    <constraint desc="" exp="" field="e"/>
    <constraint desc="" exp="" field="f"/>
    <constraint desc="" exp="" field="target_angle"/>
    <constraint desc="" exp="" field="target_scale"/>
    <constraint desc="" exp="" field="target_point"/>
    <constraint desc="" exp="" field="bounding_box"/>
  </constraintExpressions>
  <attributeactions>
    <defaultAction value="{00000000-0000-0000-0000-000000000000}" key="Canvas"/>
  </attributeactions>
  <attributetableconfig sortOrder="0" sortExpression="" actionWidgetStyle="dropDown">
    <columns>
      <column type="field" width="359" hidden="0" name="drone_map"/>
      <column type="field" width="470" hidden="0" name="path"/>
      <column type="field" width="270" hidden="0" name="prev_image"/>
      <column type="field" width="243" hidden="0" name="next_image"/>
      <column type="field" width="-1" hidden="0" name="width"/>
      <column type="field" width="-1" hidden="0" name="height"/>
      <column type="field" width="-1" hidden="0" name="lat"/>
      <column type="field" width="-1" hidden="0" name="lon"/>
      <column type="field" width="-1" hidden="0" name="altitude"/>
      <column type="field" width="-1" hidden="0" name="direction"/>
      <column type="field" width="-1" hidden="0" name="focal"/>
      <column type="field" width="-1" hidden="0" name="timestamp"/>
      <column type="field" width="-1" hidden="0" name="point"/>
      <column type="field" width="-1" hidden="0" name="a"/>
      <column type="field" width="-1" hidden="0" name="b"/>
      <column type="field" width="-1" hidden="0" name="c"/>
      <column type="field" width="-1" hidden="0" name="d"/>
      <column type="field" width="-1" hidden="0" name="e"/>
      <column type="field" width="-1" hidden="0" name="f"/>
      <column type="field" width="-1" hidden="0" name="bounding_box"/>
      <column type="actions" width="-1" hidden="1"/>
      <column type="field" width="-1" hidden="0" name="id"/>
      <column type="field" width="-1" hidden="0" name="pixel_size"/>
      <column type="field" width="-1" hidden="0" name="edges"/>
      <column type="field" width="-1" hidden="0" name="angle"/>
      <column type="field" width="-1" hidden="0" name="scale"/>
      <column type="field" width="-1" hidden="0" name="target_angle"/>
      <column type="field" width="-1" hidden="0" name="target_scale"/>
      <column type="field" width="-1" hidden="0" name="target_point"/>
    </columns>
  </attributetableconfig>
  <editform></editform>
  <editforminit/>
  <editforminitcodesource>0</editforminitcodesource>
  <editforminitfilepath></editforminitfilepath>
  <editforminitcode><![CDATA[# -*- coding: utf-8 -*-
"""
QGIS forms can have a Python function that is called when the form is
opened.

Use this function to add extra logic to your forms.

Enter the name of the function in the "Python Init function"
field.
An example follows:
"""
from qgis.PyQt.QtWidgets import QWidget

def my_form_open(dialog, layer, feature):
	geom = feature.geometry()
	control = dialog.findChild(QWidget, "MyLineEdit")
]]></editforminitcode>
  <featformsuppress>0</featformsuppress>
  <editorlayout>generatedlayout</editorlayout>
  <editable>
    <field editable="1" name="a"/>
    <field editable="1" name="altitude"/>
    <field editable="1" name="angle"/>
    <field editable="1" name="b"/>
    <field editable="1" name="bounding_box"/>
    <field editable="1" name="c"/>
    <field editable="1" name="d"/>
    <field editable="1" name="direction"/>
    <field editable="1" name="drone_map"/>
    <field editable="1" name="e"/>
    <field editable="1" name="edges"/>
    <field editable="1" name="f"/>
    <field editable="1" name="focal"/>
    <field editable="1" name="height"/>
    <field editable="1" name="id"/>
    <field editable="1" name="lat"/>
    <field editable="1" name="lon"/>
    <field editable="1" name="next_image"/>
    <field editable="1" name="path"/>
    <field editable="1" name="pixel_size"/>
    <field editable="1" name="point"/>
    <field editable="1" name="prev_image"/>
    <field editable="1" name="scale"/>
    <field editable="1" name="target_angle"/>
    <field editable="1" name="target_point"/>
    <field editable="1" name="target_scale"/>
    <field editable="1" name="timestamp"/>
    <field editable="1" name="width"/>
  </editable>
  <labelOnTop>
    <field labelOnTop="0" name="a"/>
    <field labelOnTop="0" name="altitude"/>
    <field labelOnTop="0" name="angle"/>
    <field labelOnTop="0" name="b"/>
    <field labelOnTop="0" name="bounding_box"/>
    <field labelOnTop="0" name="c"/>
    <field labelOnTop="0" name="d"/>
    <field labelOnTop="0" name="direction"/>
    <field labelOnTop="0" name="drone_map"/>
    <field labelOnTop="0" name="e"/>
    <field labelOnTop="0" name="edges"/>
    <field labelOnTop="0" name="f"/>
    <field labelOnTop="0" name="focal"/>
    <field labelOnTop="0" name="height"/>
    <field labelOnTop="0" name="id"/>
    <field labelOnTop="0" name="lat"/>
    <field labelOnTop="0" name="lon"/>
    <field labelOnTop="0" name="next_image"/>
    <field labelOnTop="0" name="path"/>
    <field labelOnTop="0" name="pixel_size"/>
    <field labelOnTop="0" name="point"/>
    <field labelOnTop="0" name="prev_image"/>
    <field labelOnTop="0" name="scale"/>
    <field labelOnTop="0" name="target_angle"/>
    <field labelOnTop="0" name="target_point"/>
    <field labelOnTop="0" name="target_scale"/>
    <field labelOnTop="0" name="timestamp"/>
    <field labelOnTop="0" name="width"/>
  </labelOnTop>
  <widgets/>
  <conditionalstyles>
    <rowstyles/>
    <fieldstyles/>
  </conditionalstyles>
  <expressionfields/>
  <previewExpression>width</previewExpression>
  <mapTip></mapTip>
  <layerGeometryType>0</layerGeometryType>
</qgis>
