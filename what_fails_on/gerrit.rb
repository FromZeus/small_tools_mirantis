begin
  require 'gerry'
rescue LoadError
  puts 'try sudo gem install gerry'
  exit
end
#require 'yaml'
require 'pp'

class Gerrit
  client = Gerry.new('https://review.fuel-infra.org')
  query =  ['q=topic:bug/819819819']
  changes = []
  failed = []
  names = []
  dict = {}
  for entries in client.changes(query)
    changes.push(entries['change_id'])
  end

  for change_id in changes
    failed_jobs = []
    query = ["q=#{change_id}&o=CURRENT_REVISION&o=MESSAGES"]
    for entries in client.changes(query)
      names.push(entries['id'])
      number = entries['revisions'][entries['current_revision']]['_number']
      for i in entries['messages']
        if number == (i['_revision_number']) and i['message'].include? 'FAILURE' and !i['message'].include? '(non-voting)'
          failed_jobs.push(i['message'])
        end
      end
    end
    failed.push(failed_jobs.last)
  end
  for i in 0..names.length-1
    dict.store(names[i], failed[i])
  end
  dict.delete_if { |k, v| v == nil }
  for k in dict.keys
    dict[k.gsub('%2F', '/').split('~')[0].split('/')[2] ] = dict.delete k
  end
  for k, v in dict
    dict[k] = v.split(' ').select {|str| str.include?('http')}[0]+'consoleFull'
  end
  list = []
  dict.each {|k, v| list.push([v, k])}
  data = YAML.load_file 'config.yaml'
  data['URLs'] = list
  File.open('config.yaml', 'w') { |file| YAML.dump(data, file)}
end
