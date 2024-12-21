#!/usr/bin/ruby

require 'pp'

# This is a little wedge that converts the gopher CGI requests into command
# line to run the web-based looking glass script

LGPATH="/var/www/localhost/htdocs/lg"

Dir.chdir LGPATH

gopher_querystr = ENV['QUERY_STRING']
if(/[^a-zA-Z0-9.-]/.match(gopher_querystr)) then
  puts("ERROR: Invalid characters in gopher query string.")
  Kernel.exit(1)
end

gopher_searchreq = ENV['SEARCHREQUEST']
if(gopher_searchreq and /[^a-zA-Z0-9.]/.match(gopher_searchreq)) then
  puts("ERROR: Invalid characters in gopher parameter.")
  Kernel.exit(1)
end

ENV['QUERY_STRING'] = "query=#{gopher_querystr}&protocol=IPv4&addr=#{gopher_searchreq}&router=KTNRONSPVR01&nodesc=y"

lg_output = `./lg.cgi`
text_started = false
lg_output.each_line do |line|
  # output everything between <CODE> and </CODE>, converting HTML characters to regular ones
  if(line.include? 'CODE>') then
    if(text_started) then
      Kernel.exit(0)
    else
      text_started = true
    end
  else
    print(line.gsub("&gt;", ">")) if text_started
  end
end
