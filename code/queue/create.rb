=begin
  
Name:         Handbrake Batch Queue Creator
Description:  A script to create a batch file for Handbrake.  
Author:       Chris W Jones chris@christopherjones.us
Date:         15 September 2014 
License: 
The MIT License (MIT)
Copyright (c) 2014 Chris W Jones
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the 'Software'), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
  
=end

def usage

"Usage:
create.rb [flags] [FILENAMES]
Create handbrake_queue.xml from FILENAMES.  The FILESNAMES file should be a list of full paths to files, one per line.
\t-f,--file [FILENAME]\tOutput queue to FILENAME instead of handbrake_queue.xml
\t-h,--help\tPrint this help
"

end

if ARGV.length==1 and ARGV[0] != '--help' and ARGV[0] != '-h'
  output_filename='handbrake_queue.xml'
  input_filename=ARGV[0]
elsif ARGV.length==3 and (ARGV[0]=='-f' or ARGV[0]=='--file')
  output_filename=ARGV[1]
  input_filename=ARGV[2]
else
  puts usage
  exit
end

input_file_handle=File.open(input_filename, 'r').read
output_file_handle=File.open(output_filename, 'w')

output_file_handle.write("
\t<?xml version='1.0'?>
\t<ArrayOfQueueTask xmlns:xsd='http://www.w3.org/2001/XMLSchema' xmlns:xsi='http://www.w3.org/2001/XMLSchema-instance'>
")
input_file_handle.each_line{|line|
  mkv_line=line.strip
  mp4_line=line.split('.')[0..-2].join+'.mp4'
  output_file_handle.write("
\t\t<QueueTask>
\t\t\t<CustomQuery>false</CustomQuery>
\t\t\t<Status>Waiting</Status>
\t\t\t<Task>
\t\t\t\t<Source>" + mkv_line + "</Source>
\t\t\t\t<Title>1</Title>
\t\t\t\t<Angle>1</Angle>
\t\t\t\t<PointToPointMode>Chapters</PointToPointMode>
\t\t\t\t<StartPoint>1</StartPoint>
\t\t\t\t<EndPoint>1</EndPoint>
\t\t\t\t<Destination>" + mp4_line + "</Destination>
\t\t\t\t<OutputFormat>Mp4</OutputFormat>
\t\t\t\t<LargeFile>false</LargeFile>
\t\t\t\t<OptimizeMP4>false</OptimizeMP4>
\t\t\t\t<IPod5GSupport>false</IPod5GSupport>
\t\t\t\t<Width>1280</Width>
\t\t\t\t<Height>0</Height>
\t\t\t\t<MaxWidth xsi:nil='true' />
\t\t\t\t<MaxHeight xsi:nil='true' />
\t\t\t\t<Cropping>
\t\t\t\t\t<Top>0</Top>
\t\t\t\t\t<Bottom>0</Bottom>
\t\t\t\t\t<Left>0</Left>
\t\t\t\t\t<Right>0</Right>
\t\t\t\t</Cropping>
\t\t\t\t<HasCropping>false</HasCropping>
\t\t\t\t<Anamorphic>Loose</Anamorphic>
\t\t\t\t<DisplayWidth xsi:nil='true' />
\t\t\t\t<KeepDisplayAspect>false</KeepDisplayAspect>
\t\t\t\t<PixelAspectX>0</PixelAspectX>
\t\t\t\t<PixelAspectY>0</PixelAspectY>
\t\t\t\t<Modulus>2</Modulus>
\t\t\t\t<Deinterlace>Off</Deinterlace>
\t\t\t\t<Decomb>Off</Decomb>
\t\t\t\t<Detelecine>Off</Detelecine>
\t\t\t\t<Denoise>Off</Denoise>
\t\t\t\t<Deblock>4</Deblock>
\t\t\t\t<Grayscale>false</Grayscale>
\t\t\t\t<VideoEncodeRateType>ConstantQuality</VideoEncodeRateType>
\t\t\t\t<VideoEncoder>X264</VideoEncoder>
\t\t\t\t<FramerateMode>VFR</FramerateMode>
\t\t\t\t<Quality>20</Quality>
\t\t\t\t<VideoBitrate xsi:nil='true' />
\t\t\t\t<TwoPass>false</TwoPass>
\t\t\t\t<TurboFirstPass>false</TurboFirstPass>
\t\t\t\t<Framerate xsi:nil='true' />
\t\t\t\t<AudioTracks>
\t\t\t\t\t<AudioTrack>
\t\t\t\t\t\t<Bitrate>160</Bitrate>
\t\t\t\t\t\t<DRC>0</DRC>
\t\t\t\t\t\t<Encoder>Faac</Encoder>
\t\t\t\t\t\t<Gain>0</Gain>
\t\t\t\t\t\t<MixDown>DolbyProLogicII</MixDown>
\t\t\t\t\t\t<SampleRate>0</SampleRate>
\t\t\t\t\t\t<SampleRateDisplayValue>Auto</SampleRateDisplayValue>
\t\t\t\t\t\t<ScannedTrack>
\t\t\t\t\t\t\t<TrackNumber>1</TrackNumber>
\t\t\t\t\t\t\t<Language>Unknown</Language>
\t\t\t\t\t\t\t<LanguageCode>und</LanguageCode>
\t\t\t\t\t\t\t<Format>AC3) (5.1 ch</Format>
\t\t\t\t\t\t\t<SampleRate>48000</SampleRate>
\t\t\t\t\t\t\t<Bitrate>384000</Bitrate>
\t\t\t\t\t\t</ScannedTrack>
\t\t\t\t\t\t<TrackName />
\t\t\t\t\t</AudioTrack>
\t\t\t\t</AudioTracks>
\t\t\t\t<AllowedPassthruOptions>
\t\t\t\t\t<AudioAllowAACPass>true</AudioAllowAACPass>
\t\t\t\t\t<AudioAllowAC3Pass>true</AudioAllowAC3Pass>
\t\t\t\t\t<AudioAllowDTSHDPass>true</AudioAllowDTSHDPass>
\t\t\t\t\t<AudioAllowDTSPass>true</AudioAllowDTSPass>
\t\t\t\t\t<AudioAllowMP3Pass>true</AudioAllowMP3Pass>
\t\t\t\t\t<AudioEncoderFallback>Ac3</AudioEncoderFallback>
\t\t\t\t</AllowedPassthruOptions>
\t\t\t\t<SubtitleTracks />
\t\t\t\t<IncludeChapterMarkers>true</IncludeChapterMarkers>
\t\t\t\t<ChapterNames>
\t\t\t\t\t<ChapterMarker>
\t\t\t\t\t\t<ChapterNumber>1</ChapterNumber>
\t\t\t\t\t\t<Duration />
\t\t\t\t\t\t<ChapterName>Chapter 1</ChapterName>
\t\t\t\t\t</ChapterMarker>
\t\t\t\t</ChapterNames>
\t\t\t\t<X264Preset>VeryFast</X264Preset>
\t\t\t\t<H264Profile>Main</H264Profile>
\t\t\t\t<H264Level>4.0</H264Level>
\t\t\t\t<X264Tune>None</X264Tune>
\t\t\t\t<FastDecode>false</FastDecode>
\t\t\t\t<PreviewStartAt xsi:nil='true' />
\t\t\t\t<PreviewDuration xsi:nil='true' />
\t\t\t\t<IsPreviewEncode>false</IsPreviewEncode>
\t\t\t\t<PreviewEncodeDuration>0</PreviewEncodeDuration>
\t\t\t\t<ShowAdvancedTab>false</ShowAdvancedTab>
\t\t\t</Task>
\t\t</QueueTask>")
}
