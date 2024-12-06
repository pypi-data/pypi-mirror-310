Facilities for ISO14496 files - the ISO Base Media File Format,
the basis for several things including MP4 and MOV.

*Latest release 20241122*:
Replace many raises of RuntimeError with NotImplementedError, suggestion by @dimaqq on disucss.python.org.

ISO make the standard available here:
* [available standards main page](http://standards.iso.org/ittf/PubliclyAvailableStandards/index.html)
* [zip file download](http://standards.iso.org/ittf/PubliclyAvailableStandards/c068960_ISO_IEC_14496-12_2015.zip)

## <a name="add_body_subclass"></a>`add_body_subclass(superclass, box_type, section, desc)`

Create and register a new `BoxBody` class that is simply a subclass of
another.
Return the new class.

## <a name="add_generic_sample_boxbody"></a>`add_generic_sample_boxbody(box_type, section, desc, struct_format_v0, sample_fields, struct_format_v1=None, has_inferred_entry_count=False)`

Create and add a specific Time to Sample box - section 8.6.1.

## <a name="add_time_to_sample_boxbody"></a>`add_time_to_sample_boxbody(box_type, section, desc)`

Add a Time to Sample box - section 8.6.1.

## <a name="Box"></a>Class `Box(cs.binary.SimpleBinary)`

Base class for all boxes - ISO14496 section 4.2.

This has the following fields:
* `header`: a `BoxHeader`
* `body`: a `BoxBody` instance, usually a specific subclass
* `unparsed`: any unconsumed bytes from the `Box` are stored as here

*`Box.BOX_TYPE`*:
The default .BOX_TYPE is inferred from the class name.

*`Box.__getattr__(self, attr)`*:
If there is no direct attribute from `SimpleBinary.__getattr__`,
have a look in the `.header` and `.body`.

*`Box.__iter__(self)`*:
Iterating over a `Box` iterates over its body.
Typically that would be the `.body.boxes`
but might be the samples if the body is a sample box,
etc.

*`Box.ancestor(self, box_type)`*:
Return the closest ancestor box of type `box_type`.

*`Box.box_type`*:
The `Box` header type.

*`Box.box_type_path`*:
The type path to this Box.

*`Box.box_type_s`*:
The `Box` header type as a string.

If the header type bytes decode as ASCII, return that,
otherwise the header bytes' repr().

*`Box.dump(self, **kw)`*:
Dump this Box.

*`Box.gather_metadata(self)`*:
Walk the `Box` hierarchy looking for metadata.
Yield `(Box,TagSet)` for each `b'moov'` or `b'trak'` `Box`.

*`Box.metatags(self)`*:
Return a `TagSet` containing metadata for this box.

*`Box.parse(bfr: cs.buffer.CornuCopyBuffer)`*:
Decode a `Box` from `bfr` and return it.

*`Box.parse_field(self, field_name, bfr: cs.buffer.CornuCopyBuffer, binary_cls)`*:
`parse_field` delegates to the `Box` body `parse_field`.

*`Box.parse_length`*:
The length of the box as consumed from the buffer,
computed as `self.end_offset-self.offset`.

*`Box.reparse_buffer(self)`*:
Context manager for continuing a parse from the `unparsed` field.

Pops the final `unparsed` field from the `Box`,
yields a `CornuCopyBuffer` make from it,
then pushes the `unparsed` field again
with the remaining contents of the buffer.

*`Box.self_check(self)`*:
Sanity check this Box.

*`Box.transcribe(self)`*:
Transcribe the `Box`.

Before transcribing the data, we compute the total box_size
from the lengths of the current header, body and unparsed
components, then set the header length if that has changed.
Since setting the header length can change its representation
we compute the length again and abort if it isn't stable.
Otherwise we proceeed with a regular transcription.

*`Box.unparsed_bs`*:
The unparsed data as a single `bytes` instance.

*`Box.user_type`*:
The header user_type.

*`Box.walk(self) -> Iterable[Tuple[ForwardRef('Box'), List[ForwardRef('Box')]]]`*:
Walk this `Box` hierarchy.

Yields the starting box and its children as `(self,subboxes)`
and then yields `(subbox,subsubboxes)` for each child in turn.

As with `os.walk`, the returned `subboxes` list
may be modified in place to prune or reorder the subsequent walk.

## <a name="BoxBody"></a>Class `BoxBody(cs.binary.SimpleBinary)`

Abstract basis for all `Box` bodies.

*`BoxBody.__getattr__(self, attr)`*:
The following virtual attributes are defined:
* *TYPE*`s`:
  "boxes of type *TYPE*",
  an uppercased box type name with a training `s`;
  a list of all elements whose `.box_type`
  equals *TYPE*`.lower().encode('ascii')`.
  The elements are obtained by iterating over `self`
  which normally means iterating over the `.boxes` attribute.
* *TYPE*:
  "the box of type *TYPE*",
  an uppercased box type name;
  the sole element whose box type matches the type,
  obtained from `.`*TYPE*`s[0]`
  with a requirement that there is exactly one match.
* *TYPE*`0`:
  "the optional box of type *TYPE*",
  an uppercased box type name with a trailing `0`;
  the sole element whose box type matches the type,
  obtained from `.`*TYPE*`s[0]`
  with a requirement that there is exactly zero or one match.
  If there are zero matches, return `None`.
  Otherwise return the matching box.

*`BoxBody.add_field(self, field_name, value)`*:
Add a field named `field_name` with the specified `value`
to the box fields.

*`BoxBody.boxbody_type_from_class()`*:
Compute the Box's 4 byte type field from the class name.

*`BoxBody.for_box_type(box_type: bytes)`*:
Return the `BoxBody` subclass suitable for the `box_type`.

*`BoxBody.parse(bfr: cs.buffer.CornuCopyBuffer)`*:
Create a new instance and gather the `Box` body fields from `bfr`.

Subclasses implement a `parse_fields` method to parse additional fields.

*`BoxBody.parse_boxes(self, bfr: cs.buffer.CornuCopyBuffer, **kw)`*:
Utility method to parse the remainder of the buffer as a
sequence of `Box`es.

*`BoxBody.parse_field(self, field_name, bfr: cs.buffer.CornuCopyBuffer, binary_cls)`*:
Parse an instance of `binary_cls` from `bfr`
and store it as the attribute named `field_name`.

`binary_cls` may also be an `int`, in which case that many
bytes are read from `bfr`.

*`BoxBody.parse_field_value(self, field_name, bfr: cs.buffer.CornuCopyBuffer, binary_cls)`*:
Parse a single value binary, store the value as `field_name`,
store the instance as the field `field_name+'__Binary'`
for transcription.

Note that this disassociaes the plain value attribute
from what gets transcribed.

*`BoxBody.parse_fields(self, bfr: cs.buffer.CornuCopyBuffer)`*:
Parse additional fields.
This base class implementation consumes nothing.

*`BoxBody.transcribe(self)`*:
Transcribe the binary structure.

This default implementation transcribes the fields parsed with the
`parse_field` method in the order parsed.

*`BoxBody.transcribe_fields(self)`*:
Transcribe the fields parsed with the `parse_field` method in the
order parsed.

## <a name="BoxHeader"></a>Class `BoxHeader(cs.binary.BoxHeader)`

An ISO14496 `Box` header packet.

*`BoxHeader.parse(bfr: cs.buffer.CornuCopyBuffer)`*:
Decode a box header from `bfr`.

## <a name="BTRTBoxBody"></a>Class `BTRTBoxBody(BoxBody)`

BitRateBoxBody - section 8.5.2.2.

*`BTRTBoxBody.parse_fields(self, bfr: cs.buffer.CornuCopyBuffer)`*:
Gather the `bufferSizeDB`, `maxBitrate` and `avgBitrate` fields.

## <a name="CO64BoxBody"></a>Class `CO64BoxBody(FullBoxBody)`

A 'c064' Chunk Offset box - section 8.7.5.

*`CO64BoxBody.parse_fields(self, bfr: cs.buffer.CornuCopyBuffer)`*:
Gather the `entry_count` and `chunk_offsets` fields.

*`CO64BoxBody.transcribe(self)`*:
Transcribe a `CO64BoxBody`.

## <a name="ContainerBoxBody"></a>Class `ContainerBoxBody(BoxBody)`

Common subclass of several things with `.boxes`.

## <a name="CPRTBoxBody"></a>Class `CPRTBoxBody(FullBoxBody)`

A 'cprt' Copyright box - section 8.10.2.

*`CPRTBoxBody.language`*:
The `language_field` as the 3 character ISO 639-2/T language code.

*`CPRTBoxBody.parse_fields(self, bfr: cs.buffer.CornuCopyBuffer)`*:
Gather the `language` and `notice` fields.

## <a name="CSLGBoxBody"></a>Class `CSLGBoxBody(FullBoxBody)`

A 'cslg' Composition to Decode box - section 8.6.1.4.

*`CSLGBoxBody.CSLGParamsLong`*

*`CSLGBoxBody.CSLGParamsQuad`*

*`CSLGBoxBody.__getattr__(self, attr)`*:
Present the `params` attributes at the top level.

*`CSLGBoxBody.parse_fields(self, bfr: cs.buffer.CornuCopyBuffer)`*:
Gather the compositionToDTSShift`, `leastDecodeToDisplayDelta`,
`greatestDecodeToDisplayDelta`, `compositionStartTime` and
`compositionEndTime` fields.

## <a name="decode_itunes_date_field"></a>`decode_itunes_date_field(data) -> datetime.datetime`

The iTunes 'Date' meta field: a year or an ISO timestamp.

## <a name="deref_box"></a>`deref_box(B, path)`

Dereference a path with respect to this Box.

## <a name="DREFBoxBody"></a>Class `DREFBoxBody(FullBoxBody)`

A 'dref' Data Reference box containing Data Entry boxes - section 8.7.2.1.

*`DREFBoxBody.parse_fields(self, bfr: cs.buffer.CornuCopyBuffer)`*:
Gather the `entry_count` and `boxes` fields.

## <a name="dump_box"></a>`dump_box(B, indent='', fp=None, crop_length=170, indent_incr=None)`

Recursively dump a Box.

## <a name="ELNGBoxBody"></a>Class `ELNGBoxBody(FullBoxBody)`

A ELNGBoxBody is a Extended Language Tag box - ISO14496 section 8.4.6.

*`ELNGBoxBody.parse_fields(self, bfr: cs.buffer.CornuCopyBuffer)`*:
Gather the `extended_language` field.

## <a name="ELSTBoxBody"></a>Class `ELSTBoxBody(FullBoxBody)`

An 'elst' Edit List FullBoxBody - section 8.6.6.

*`ELSTBoxBody.V0EditEntry`*

*`ELSTBoxBody.V1EditEntry`*

*`ELSTBoxBody.entry_class`*:
The class representing each entry.

*`ELSTBoxBody.entry_count`*:
The number of entries.

*`ELSTBoxBody.parse_fields(self, bfr: cs.buffer.CornuCopyBuffer)`*:
Parse the fields of an `ELSTBoxBody`.

*`ELSTBoxBody.transcribe(self)`*:
Transcribe an `ELSTBoxBody`.

## <a name="FREEBoxBody"></a>Class `FREEBoxBody(BoxBody)`

A 'free' or 'skip' box - ISO14496 section 8.1.2.
Note the length and discard the data portion.

*`FREEBoxBody.parse_fields(self, bfr: cs.buffer.CornuCopyBuffer, end_offset=Ellipsis, **kw)`*:
Gather the `padding` field.

## <a name="FTYPBoxBody"></a>Class `FTYPBoxBody(BoxBody)`

An 'ftyp' File Type box - ISO14496 section 4.3.
Decode the major_brand, minor_version and compatible_brands.

*`FTYPBoxBody.compatible_brands`*:
The compatible brands as a list of 4 byte bytes instances.

*`FTYPBoxBody.parse_fields(self, bfr: cs.buffer.CornuCopyBuffer, **kw)`*:
Gather the `major_brand`, `minor_version` and `brand_bs` fields.

## <a name="FullBoxBody"></a>Class `FullBoxBody(BoxBody)`

A common extension of a basic BoxBody, with a version and flags field.
ISO14496 section 4.2.

*`FullBoxBody.flags`*:
The flags value, computed from the 3 flag bytes.

## <a name="get_deref_path"></a>`get_deref_path(path, offset=0)`

Parse a `path` string from `offset`.
Return the path components and the offset where the parse stopped.

Path components:
* _identifier_: an identifier represents a `Box` field or if such a
  field is not present, a the first subbox of this type
* `[`_index_`]`: the subbox with index _index_

Examples:

    >>> get_deref_path('.abcd[5]')
    (['abcd', 5], 8)

## <a name="HDLRBoxBody"></a>Class `HDLRBoxBody(FullBoxBody)`

A HDLRBoxBody is a Handler Reference box - ISO14496 section 8.4.3.

*`HDLRBoxBody.handler_type`*:
The handler_type as an ASCII string, its usual form.

*`HDLRBoxBody.parse_fields(self, bfr: cs.buffer.CornuCopyBuffer)`*:
Gather the `handler_type_long` and `name` fields.

## <a name="ILSTAofBSchema"></a>`ILSTAofBSchema(attribute_name)`

Attribute name and type for ILST "A of B" schema.

## <a name="ILSTBoxBody"></a>Class `ILSTBoxBody(ContainerBoxBody)`

Apple iTunes Information List, container for iTunes metadata fields.

The basis of the format knowledge here comes from AtomicParsley's
documentation here:

    http://atomicparsley.sourceforge.net/mpeg-4files.html

and additional information from:

    https://github.com/sergiomb2/libmp4v2/wiki/iTunesMetadata

*`ILSTBoxBody.parse_fields(self, bfr: cs.buffer.CornuCopyBuffer)`*:
pylint: disable=attribute-defined-outside-init,too-many-locals
pylint: disable=too-many-statements,too-many-branches

## <a name="ILSTISOFormatSchema"></a>`ILSTISOFormatSchema(attribute_name)`

Attribute name and type for ILST ISO format schema.

## <a name="ILSTRawSchema"></a>`ILSTRawSchema(attribute_name)`

Attribute name and type for ILST raw schema.

## <a name="ILSTTextSchema"></a>`ILSTTextSchema(attribute_name)`

Attribute name and type for ILST text schema.

## <a name="ILSTUInt32BESchema"></a>`ILSTUInt32BESchema(attribute_name)`

Attribute name and type for ILST `UInt32BE` schema.

## <a name="ILSTUInt8Schema"></a>`ILSTUInt8Schema(attribute_name)`

Attribute name and type for ILST `UInt8BE` schema.

## <a name="itunes_media_type"></a>Class `itunes_media_type(builtins.tuple)`

itunes_media_type(type, stik)

*`itunes_media_type.stik`*:
Alias for field number 1

*`itunes_media_type.type`*:
Alias for field number 0

## <a name="itunes_store_country_code"></a>Class `itunes_store_country_code(builtins.tuple)`

itunes_store_country_code(country_name, iso_3166_1_code, itunes_store_code)

*`itunes_store_country_code.country_name`*:
Alias for field number 0

*`itunes_store_country_code.iso_3166_1_code`*:
Alias for field number 1

*`itunes_store_country_code.itunes_store_code`*:
Alias for field number 2

## <a name="main"></a>`main(argv=None)`

Command line mode.

## <a name="MDATBoxBody"></a>Class `MDATBoxBody(BoxBody)`

A Media Data Box - ISO14496 section 8.1.1.

*`MDATBoxBody.parse_fields(self, bfr: cs.buffer.CornuCopyBuffer)`*:
Gather all data to the end of the field.

*`MDATBoxBody.transcribe(self)`*:
Transcribe the data.
Raise an `AssertionError` if we skipped the data during the parse.

*`MDATBoxBody.transcribed_length(self)`*:
Return the transcription length even if we didn't keep the data.

## <a name="MDHDBoxBody"></a>Class `MDHDBoxBody(FullBoxBody)`

A MDHDBoxBody is a Media Header box - ISO14496 section 8.4.2.

*`MDHDBoxBody.parse_fields(self, bfr: cs.buffer.CornuCopyBuffer)`*:
Gather the `creation_time`, `modification_time`, `timescale`,
`duration` and `language_short` fields.

## <a name="METABoxBody"></a>Class `METABoxBody(FullBoxBody)`

A 'meta' Meta BoxBody - section 8.11.1.

*`METABoxBody.__getattr__(self, attr)`*:
Present the `ilst` attributes if present.

*`METABoxBody.parse_fields(self, bfr: cs.buffer.CornuCopyBuffer)`*:
Gather the `theHandler` `Box` and gather the following Boxes as `boxes`.

## <a name="MOOVBoxBody"></a>Class `MOOVBoxBody(ContainerBoxBody)`

An 'moov' Movie box - ISO14496 section 8.2.1.
Decode the contained boxes.

## <a name="MVHDBoxBody"></a>Class `MVHDBoxBody(FullBoxBody)`

An 'mvhd' Movie Header box - ISO14496 section 8.2.2.

## <a name="OverBox"></a>Class `OverBox(cs.binary.BinaryListValues, HasBoxesMixin)`

A fictitious `Box` encompassing all the Boxes in an input buffer.

*`OverBox.boxes`*:
Alias `.value` as `.boxes`: the `Box`es encompassed by this `OverBox`.

*`OverBox.dump(self, **kw)`*:
Dump this OverBox.

*`OverBox.length`*:
The `OverBox` is as long as the subsidary Boxes.

*`OverBox.parse(bfr: cs.buffer.CornuCopyBuffer)`*:
Parse the `OverBox`.

*`OverBox.walk(self)`*:
Walk the `Box`es in the `OverBox`.

This does not yield the `OverBox` itself, it isn't really a `Box`.

## <a name="parse"></a>`parse(o)`

Return the `OverBox` from a source (str, int, bytes, file).

The leading `o` parameter may be one of:
* `str`: a filesystem file pathname
* `int`: a OS file descriptor
* `bytes`: a `bytes` object
* `file`: if not `int` or `str` the presumption
  is that this is a file-like object

Keyword arguments are as for `OverBox.from_buffer`.

## <a name="parse_fields"></a>`parse_fields(bfr, copy_offsets=None, **kw)`

Parse an ISO14496 stream from the CornuCopyBuffer `bfr`,
yield top level OverBoxes.

Parameters:
* `bfr`: a `CornuCopyBuffer` provided the stream data,
  preferably seekable
* `discard_data`: whether to discard unparsed data, default `False`
* `copy_offsets`: callable to receive `Box` offsets

## <a name="parse_tags"></a>`parse_tags(path, tag_prefix=None)`

Parse the tags from `path`.
Yield `(box,tags)` for each subbox with tags.

The optional `tag_prefix` parameter
may be specified to prefix each tag name with a prefix.
Other keyword arguments are passed to `parse()`
(typical example: `discard_data=True`).

## <a name="PDINBoxBody"></a>Class `PDINBoxBody(FullBoxBody)`

A 'pdin' Progressive Download Information box - ISO14496 section 8.1.3.

*`PDINBoxBody.PDInfo`*

*`PDINBoxBody.parse_fields(self, bfr: cs.buffer.CornuCopyBuffer, **kw)`*:
Gather the normal version information
and then the `(rate,initial_delay)` pairs of the data section
as the `pdinfo` field.

## <a name="report"></a>`report(box, indent='', fp=None, indent_incr=None)`

Report some human friendly information about a box.

## <a name="SMHDBoxBody"></a>Class `SMHDBoxBody(FullBoxBody)`

A 'smhd' Sound Media Headerbox - section 12.2.2.

*`SMHDBoxBody.parse_fields(self, bfr: cs.buffer.CornuCopyBuffer)`*:
Gather the `balance` field.

## <a name="STCOBoxBody"></a>Class `STCOBoxBody(FullBoxBody)`

A 'stco' Chunk Offset box - section 8.7.5.

*`STCOBoxBody.chunk_offsets`*:
Parse the `UInt32BE` chunk offsets from stashed buffer.

*`STCOBoxBody.parse_fields(self, bfr: cs.buffer.CornuCopyBuffer)`*:
Gather the `entry_count` and `chunk_offsets` fields.

## <a name="STSCBoxBody"></a>Class `STSCBoxBody(FullBoxBody)`

'stsc' (Sample Table box - section 8.7.4.1.

*`STSCBoxBody.STSCEntry`*

*`STSCBoxBody.entries`*:
A list of `int`s parsed from the `STSCEntry` list.

*`STSCBoxBody.parse_fields(self, bfr: cs.buffer.CornuCopyBuffer)`*:
Gather the `entry_count` and `entries` fields.

## <a name="STSZBoxBody"></a>Class `STSZBoxBody(FullBoxBody)`

A 'stsz' Sample Size box - section 8.7.3.2.

*`STSZBoxBody.entry_sizes`*:
Parse the `UInt32BE` entry sizes from stashed buffer
into a list of `int`s.

*`STSZBoxBody.parse_fields(self, bfr: cs.buffer.CornuCopyBuffer)`*:
Gather the `sample_size`, `sample_count`, and `entry_sizes` fields.

*`STSZBoxBody.transcribe(self)`*:
Transcribe the `STSZBoxBody`.

## <a name="STZ2BoxBody"></a>Class `STZ2BoxBody(FullBoxBody)`

A 'stz2' Compact Sample Size box - section 8.7.3.3.

*`STZ2BoxBody.parse_fields(self, bfr: cs.buffer.CornuCopyBuffer)`*:
Gather the `field_size`, `sample_count` and `entry_sizes` fields.

*`STZ2BoxBody.transcribe(self)`*:
transcribe the STZ2BoxBody.

## <a name="TimeStamp32"></a>Class `TimeStamp32(cs.binary.UInt32BE, TimeStampMixin)`

The 32 bit form of an ISO14496 timestamp.

## <a name="TimeStamp64"></a>Class `TimeStamp64(cs.binary.UInt64BE, TimeStampMixin)`

The 64 bit form of an ISO14496 timestamp.

## <a name="TimeStampMixin"></a>Class `TimeStampMixin`

Methods to assist with ISO14496 timestamps.

*`TimeStampMixin.datetime`*:
This timestamp as an UTC datetime.

*`TimeStampMixin.unixtime`*:
This timestamp as a UNIX time (seconds since 1 January 1970).

## <a name="TKHDBoxBody"></a>Class `TKHDBoxBody(FullBoxBody)`

A 'tkhd' Track Header box - ISO14496 section 8.2.2.

*`TKHDBoxBody.TKHDMatrix`*

## <a name="TrackGroupTypeBoxBody"></a>Class `TrackGroupTypeBoxBody(FullBoxBody)`

A TrackGroupTypeBoxBody contains a track group id - ISO14496 section 8.3.3.2.

*`TrackGroupTypeBoxBody.parse_fields(self, bfr: cs.buffer.CornuCopyBuffer)`*:
Gather the `track_group_id` field.

## <a name="TrackReferenceTypeBoxBody"></a>Class `TrackReferenceTypeBoxBody(BoxBody)`

A TrackReferenceTypeBoxBody contains references to other tracks - ISO14496 section 8.3.3.2.

*`TrackReferenceTypeBoxBody.parse_fields(self, bfr: cs.buffer.CornuCopyBuffer)`*:
Gather the `track_ids` field.

## <a name="TREFBoxBody"></a>Class `TREFBoxBody(ContainerBoxBody)`

Track Reference BoxBody, container for trackReferenceTypeBoxes - ISO14496 section 8.3.3.

## <a name="TTSB_Sample"></a>Class `TTSB_Sample(builtins.tuple)`

TTSB_Sample(count, delta)

*`TTSB_Sample.count`*:
Alias for field number 0

*`TTSB_Sample.delta`*:
Alias for field number 1

## <a name="URL_BoxBody"></a>Class `URL_BoxBody(FullBoxBody)`

An 'url ' Data Entry URL BoxBody - section 8.7.2.1.

*`URL_BoxBody.parse_fields(self, bfr: cs.buffer.CornuCopyBuffer)`*:
Gather the `location` field.

## <a name="URN_BoxBody"></a>Class `URN_BoxBody(FullBoxBody)`

An 'urn ' Data Entry URL BoxBody - section 8.7.2.1.

*`URN_BoxBody.parse_fields(self, bfr: cs.buffer.CornuCopyBuffer)`*:
Gather the `name` and `location` fields.

## <a name="UTF8or16Field"></a>Class `UTF8or16Field(cs.binary.SimpleBinary)`

An ISO14496 UTF8 or UTF16 encoded string.

*`UTF8or16Field.parse(bfr: cs.buffer.CornuCopyBuffer)`*:
Gather optional BOM and then UTF8 or UTF16 string.

*`UTF8or16Field.transcribe(self)`*:
Transcribe the field suitably encoded.

## <a name="VMHDBoxBody"></a>Class `VMHDBoxBody(FullBoxBody)`

A 'vmhd' Video Media Headerbox - section 12.1.2.

*`VMHDBoxBody.OpColor`*

*`VMHDBoxBody.parse_fields(self, bfr: cs.buffer.CornuCopyBuffer)`*:
Gather the `graphicsmode` and `opcolor` fields.

# Release Log



*Release 20241122*:
Replace many raises of RuntimeError with NotImplementedError, suggestion by @dimaqq on disucss.python.org.

*Release 20240422*:
* Replace dropped UTF16NULField with BinaryUTF16NUL.
* Comment out unused CO64BoxBody.chunk_offsets, uses dropped (and not replaced) deferred_field.
* Drop FallbackBoxBody, we'll just use BoxBody when there's no box specific subclass.
* Replace pick_boxbody_class with BoxBody.for_box_type.
* Rename boxbody_type_from_klass to boxbody_type_from_class.
* Drop obsolete KNOWN_BOXBODY_CLASSES.
* MP4Command.cmd_info: print moov.udta.meta.ilst.cover in SIXEL format on a terminal.
* Rename parse_deref_path to get_deref_path like other lexical functions.
* ILSTBoxBody.__getattr__: fix lookup of long names.

*Release 20231129*:
Small updates and fixes.

*Release 20230212*:
* Drop cs.context.StackableState in favour of cs.threads.State.
* MP4Command.cmd_autotag: use @uses_fstags for the fstags parameter.

*Release 20220606*:
Update obsolete use of Tag.with_prefix.

*Release 20210306*:
* Huge refactor of the Box classes to the new Binary* classes from cs.binary.
* mp4: new "tags" subcommand to print the tags parsed from a file.
* BoxHeader: fix the definition of MAX_BOX_SIZE_32.
* BoxBody: new parse_boxes utility method to part the remainder of a Box as subBoxes.
* MP4.cmd_parse: run the main parse in discard_data=True mode.
* METABoxBody.__getattr__: fix ILST typo.
* MP4Command: update for new cs.cmdutils.BaseCommand API.
* Many small fixes and tweaks.

*Release 20200229*:
* ILST: recognise @cpy as copyright, sfID as itunes_store_country_code.
* ILST: new SFID_ISO_3166_1_ALPHA_3_CODE and STIK_MEDIA_TYPES providing context data for various field values, as yet unused.
* Make various list fields of some boxes deferred because they are expensive to parse (uses new cs.binary deferred_field).
* add_generic_sample_boxbody: drop __iter__, causes dumb iterators to parse the samples.
* ILST: iTunes "Date" metadata seem to contain plain years or ISO8601 datestamps.
* mp4 autotag: add -n (no action) and -p,--prefix (set tag prefix, default 'mp4') options.
* mp4 autotag: use "mp4." as the tag prefix.

*Release 20200130*:
* Parsing of ILST boxes (iTunes metadata).
* Command line: new "info" subcommand reporting metadata, "autotag" applying metadata to fstags.
* Box tree walk, ancestor, iteration.
* Assorted cleanups and internal changes.

*Release 20190220*:
parse_buffer yields instead of returns; some small bugfixes.

*Release 20180810*:
* parse_fd(): use a mmap to access the descriptor if a regular file and not discard_data;
* this lets us use the mmapped file as backing store for the data, a big win for the media sections.

*Release 20180805*:
Initial PyPI release.
